# Create your views here.
from django.apps import apps
from django.core.serializers import serialize
from django.db.models import Count, Case, CharField, Value, When, Avg, Min, Max
from django.http import HttpResponse
from django.views import generic
from django.views.generic import TemplateView
from pytz import unicode
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from braces.views import GroupRequiredMixin
from django_tables2 import RequestConfig
from django_tables2 import MultiTableMixin
from rest_framework_swagger.views import get_swagger_view

from .tables import *
from .serializers import *
from .models import *

schema_view = get_swagger_view(title='V2OFDjango API')


class HomePageView(TemplateView):
    template_name = 'home.html'


class MKPageView(TemplateView):
    template_name = 'mk/base.html'


class MapPageView(TemplateView):
    template_name = 'gis/index.html'


class GeneralViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)

    @property
    def model(self):
        return apps.get_model(app_label=str(self.kwargs['app_label']), model_name=str(self.kwargs['model_name']))

    def get_queryset(self):
        model = self.model
        return model.objects.all()

    def get_serializer_class(self):
        GeneralSerializer.Meta.model = self.model
        return GeneralSerializer


class UserCreate(generics.CreateAPIView):
    authentication_classes = ()
    permission_classes = ()
    serializer_class = V2OfUsersSerializer


# ViewSets define the view behavior.
class UserViewSet(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticated,)
    queryset = V2OfUsers.objects.all()
    serializer_class = V2OfUsersSerializer

    def get(self, request, format=None):
        content = {
            'user': unicode(request.user),  # `django.contrib.auth.User` instance.
            'auth': unicode(request.auth),  # None
        }
        return Response(content)


class OperatorView(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Measurements.objects.distinct("operatorname").all()
    serializer_class = MeasurementsSerializer

    def get_queryset(self):
        """ allow rest api to filter by operatorname """
        queryset = Measurements.objects.distinct("operatorname").all()
        operatorname = self.request.query_params.get('operatorname', None)
        if operatorname is not None:
            queryset = queryset.filter(operatorname=operatorname)
        return queryset


class MeasurementsView(generics.ListCreateAPIView):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Measurements.objects.all()[:50]

    serializer_class = MeasurementsSerializer


# Geojson serializer
def geojsonFeed(request):
    return HttpResponse(serialize('geojson', V2OfAreas.objects.all(), fields=('name', 'area')))


class CampaignsListView(GroupRequiredMixin, generic.ListView):
    model = V2OfCampaigns
    context_object_name = 'campaign'
    queryset = model.objects.all()
    ordering = ['id']
    group_required = u'active'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['nav_campaign'] = True
        CampaignsTab = CampaignsTable(V2OfCampaigns.objects.all(),
                                      template_name='django_tables2/bootstrap-responsive.html')
        RequestConfig(self.request, paginate={'per_page': 30}).configure(CampaignsTab)
        context['table'] = CampaignsTab
        return context


class CampaignsDetailView(generic.DetailView):
    model = V2OfCampaigns


# Count all Providers (i.e COSMOTE, VODAFONE, WIND)
class CountView(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Measurements.objects.annotate(key=Case(When(operatorname__icontains='wind', then=Value('WIND')),
                                                      When(operatorname__icontains='vodafone',
                                                           then=Value('VODAFONE')),
                                                      When(operatorname__icontains='cosmote',
                                                           then=Value('COSMOTE')),
                                                      default=Value('OTHER'), output_field=CharField(), ),
                                             ).values('key').annotate(value=Count('operatorname')).order_by()
    serializer_class = CountSerializer

    def get_queryset(self):
        """ allow rest api to filter by network type (i.e. 2G, 3G, 4G)"""

        queryset = Measurements.objects.annotate(
            key=Case(When(operatorname__icontains='wind', then=Value('WIND')),
                     When(operatorname__icontains='vodafone',
                          then=Value('VODAFONE')),
                     When(operatorname__icontains='cosmote',
                          then=Value('COSMOTE')),
                     default=Value('OTHER'), output_field=CharField(), ),
        ).values('key').annotate(value=Count('operatorname')).order_by()

        network_type = self.request.query_params.get('network_type', None)
        if network_type is not None:
            queryset = queryset.filter(network_type__icontains=network_type)
        return queryset

    # Statistic Bar Charts View


class StatisticsView(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = Measurements.objects.annotate(key=Case(When(operatorname__icontains='wind', then=Value('WIND')),
                                                      When(operatorname__icontains='vodafone',
                                                           then=Value('VODAFONE')),
                                                      When(operatorname__icontains='cosmote',
                                                           then=Value('COSMOTE')),
                                                      default=Value('OTHER'), output_field=CharField(), ),
                                             ).values('key').annotate(avg=Avg('level'),
                                                                      min=Min('level'),
                                                                      max=Max('level'))

    serializer_class = GlobalSerializer

    def get_queryset(self):
        """ allow rest api to filter by min, max, avg for all Providers"""

        queryset = Measurements.objects.annotate(
            key=Case(When(operatorname__icontains='wind', then=Value('WIND')),
                     When(operatorname__icontains='vodafone',
                          then=Value('VODAFONE')),
                     When(operatorname__icontains='cosmote',
                          then=Value('COSMOTE')),
                     default=Value('OTHER'), output_field=CharField(), ),
        ).values('key').annotate(avg=Avg('level'),
                                 min=Min('level'),
                                 max=Max('level'))

        operatorname = self.request.query_params.get('operatorname', None)
        if operatorname is not None:
            queryset = queryset.filter(key=operatorname)
        return queryset

    # Statistic View for All Providers and Network Types with operatorname params


class StatisticsNetworkView(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    queryset = Measurements.objects.annotate(key=Case(When(operatorname__icontains='wind', then=Value('WIND')),
                                                      When(operatorname__icontains='vodafone',
                                                           then=Value('VODAFONE')),
                                                      When(operatorname__icontains='cosmote',
                                                           then=Value('COSMOTE')),
                                                      default=Value('OTHER'), output_field=CharField(), ),
                                             ).values('key').annotate(avg=Avg('level'),
                                                                      min=Min('level'),
                                                                      max=Max('level'))

    serializer_class = GlobalSerializer

    def get_queryset(self):
        """ allow rest api to filter by min, max, avg for all Providers"""

        queryset = Measurements.objects.annotate(
            key=Case(When(operatorname__icontains='wind', then=Value('WIND')),
                     When(operatorname__icontains='vodafone',
                          then=Value('VODAFONE')),
                     When(operatorname__icontains='cosmote',
                          then=Value('COSMOTE')),
                     default=Value('OTHER'), output_field=CharField(), ),
        ).values('key').annotate(avg=Avg('level'),
                                 min=Min('level'),
                                 max=Max('level'))

        network_type = self.kwargs.get('network_type', None)
        return queryset.filter(network_type__icontains=network_type)


# Statistics View for All Providers and Network Types with date range params


class StatisticsDateView(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Measurements.objects.annotate(key=Case(When(operatorname__icontains='wind', then=Value('WIND')),
                                                      When(operatorname__icontains='vodafone',
                                                           then=Value('VODAFONE')),
                                                      When(operatorname__icontains='cosmote',
                                                           then=Value('COSMOTE')),
                                                      default=Value('OTHER'), output_field=CharField(), ),
                                             ).values('key').annotate(avg=Avg('level'),
                                                                      min=Min('level'),
                                                                      max=Max('level'))
    serializer_class = GlobalSerializer

    def get_queryset(self):
        """ allow rest api to filter by timestamp """
        queryset = Measurements.objects.annotate(
            key=Case(When(operatorname__icontains='wind', then=Value('WIND')),
                     When(operatorname__icontains='vodafone',
                          then=Value('VODAFONE')),
                     When(operatorname__icontains='cosmote',
                          then=Value('COSMOTE')),
                     default=Value('OTHER'), output_field=CharField(), ),
        ).values('key').annotate(avg=Avg('level'),
                                 min=Min('level'),
                                 max=Max('level'))

        start_date = self.kwargs.get('start')
        end_date = self.kwargs.get('end')
        return queryset.filter(timestamp__gte=start_date, timestamp__lte=end_date)

    # Statistics View for All Providers and Network Types with date range params
    # and Network Type params


class StatisticsDateNetworkView(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Measurements.objects.annotate(key=Case(When(operatorname__icontains='wind', then=Value('WIND')),
                                                      When(operatorname__icontains='vodafone',
                                                           then=Value('VODAFONE')),
                                                      When(operatorname__icontains='cosmote',
                                                           then=Value('COSMOTE')),
                                                      default=Value('OTHER'), output_field=CharField(), ),
                                             ).values('key').annotate(avg=Avg('level'),
                                                                      min=Min('level'),
                                                                      max=Max('level'))
    serializer_class = GlobalSerializer

    def get_queryset(self):
        """ allow rest api to filter by timestamp """
        queryset = Measurements.objects.annotate(
            key=Case(When(operatorname__icontains='wind', then=Value('WIND')),
                     When(operatorname__icontains='vodafone',
                          then=Value('VODAFONE')),
                     When(operatorname__icontains='cosmote',
                          then=Value('COSMOTE')),
                     default=Value('OTHER'), output_field=CharField(), ),
        ).values('key').annotate(avg=Avg('level'),
                                 min=Min('level'),
                                 max=Max('level'))

        start_date = self.kwargs.get('start')
        end_date = self.kwargs.get('end')
        network_type = self.kwargs.get('network_type', None)
        return queryset.filter(network_type__icontains=network_type, timestamp__gte=start_date,
                               timestamp__lte=end_date)


# Up Link View for All Providers and Network Types with operatorname params

class UpLinkView(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Measurements.objects.annotate(key=Case(When(operatorname__icontains='wind', then=Value('WIND')),
                                                      When(operatorname__icontains='vodafone',
                                                           then=Value('VODAFONE')),
                                                      When(operatorname__icontains='cosmote',
                                                           then=Value('COSMOTE')),
                                                      default=Value('OTHER'), output_field=CharField(), ),
                                             ).values('key').annotate(avg=Avg('ul_bitrate'),
                                                                      min=Min('ul_bitrate'),
                                                                      max=Max('ul_bitrate'))
    serializer_class = GlobalSerializer

    def get_queryset(self):
        """ allow rest api to filter by network type """
        queryset = Measurements.objects.annotate(
            key=Case(When(operatorname__icontains='wind', then=Value('WIND')),
                     When(operatorname__icontains='vodafone',
                          then=Value('VODAFONE')),
                     When(operatorname__icontains='cosmote',
                          then=Value('COSMOTE')),
                     default=Value('OTHER'), output_field=CharField(), ),
        ).values('key').annotate(avg=Avg('ul_bitrate'),
                                 min=Min('ul_bitrate'),
                                 max=Max('ul_bitrate'))

        operatorname = self.request.query_params.get('operatorname', None)
        if operatorname is not None:
            queryset = queryset.filter(operatorname__icontains=operatorname)
        return queryset


# Up Link View for All Providers and Network Types with network type parameters

class UpLinkNetworkView(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Measurements.objects.annotate(key=Case(When(operatorname__icontains='wind', then=Value('WIND')),
                                                      When(operatorname__icontains='vodafone',
                                                           then=Value('VODAFONE')),
                                                      When(operatorname__icontains='cosmote',
                                                           then=Value('COSMOTE')),
                                                      default=Value('OTHER'), output_field=CharField(), ),
                                             ).values('key').annotate(avg=Avg('ul_bitrate'),
                                                                      min=Min('ul_bitrate'),
                                                                      max=Max('ul_bitrate'))
    serializer_class = GlobalSerializer

    def get_queryset(self):
        """ allow rest api to filter by network type """
        queryset = Measurements.objects.annotate(
            key=Case(When(operatorname__icontains='wind', then=Value('WIND')),
                     When(operatorname__icontains='vodafone',
                          then=Value('VODAFONE')),
                     When(operatorname__icontains='cosmote',
                          then=Value('COSMOTE')),
                     default=Value('OTHER'), output_field=CharField(), ),
        ).values('key').annotate(avg=Avg('ul_bitrate'),
                                 min=Min('ul_bitrate'),
                                 max=Max('ul_bitrate'))

        network_type = self.kwargs.get('network_type', None)
        # network_type = self.request.query_params.get('network_type', None)
        # if network_type is not None:
        #   queryset = queryset.filter(network_type__icontains=network_type)
        return queryset.filter(network_type__icontains=network_type)

    # Up Link View for All Providers and Network Types with date range params


class UpLinkDateView(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Measurements.objects.annotate(key=Case(When(operatorname__icontains='wind', then=Value('WIND')),
                                                      When(operatorname__icontains='vodafone',
                                                           then=Value('VODAFONE')),
                                                      When(operatorname__icontains='cosmote',
                                                           then=Value('COSMOTE')),
                                                      default=Value('OTHER'), output_field=CharField(), ),
                                             ).values('key').annotate(avg=Avg('ul_bitrate'),
                                                                      min=Min('ul_bitrate'),
                                                                      max=Max('ul_bitrate'))
    serializer_class = GlobalSerializer

    def get_queryset(self):
        """ allow rest api to filter by timestamp """
        queryset = Measurements.objects.annotate(
            key=Case(When(operatorname__icontains='wind', then=Value('WIND')),
                     When(operatorname__icontains='vodafone',
                          then=Value('VODAFONE')),
                     When(operatorname__icontains='cosmote',
                          then=Value('COSMOTE')),
                     default=Value('OTHER'), output_field=CharField(), ),
        ).values('key').annotate(avg=Avg('ul_bitrate'),
                                 min=Min('ul_bitrate'),
                                 max=Max('ul_bitrate'))

        start_date = self.kwargs.get('start')
        end_date = self.kwargs.get('end')
        return queryset.filter(timestamp__gte=start_date, timestamp__lte=end_date)

    # Up Link View for All Providers and Network Types with date range params
    # and Network Type params


class UpLinkDateNetworkView(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Measurements.objects.annotate(key=Case(When(operatorname__icontains='wind', then=Value('WIND')),
                                                      When(operatorname__icontains='vodafone',
                                                           then=Value('VODAFONE')),
                                                      When(operatorname__icontains='cosmote',
                                                           then=Value('COSMOTE')),
                                                      default=Value('OTHER'), output_field=CharField(), ),
                                             ).values('key').annotate(avg=Avg('ul_bitrate'),
                                                                      min=Min('ul_bitrate'),
                                                                      max=Max('ul_bitrate'))
    serializer_class = GlobalSerializer

    def get_queryset(self):
        """ allow rest api to filter by timestamp """
        queryset = Measurements.objects.annotate(
            key=Case(When(operatorname__icontains='wind', then=Value('WIND')),
                     When(operatorname__icontains='vodafone',
                          then=Value('VODAFONE')),
                     When(operatorname__icontains='cosmote',
                          then=Value('COSMOTE')),
                     default=Value('OTHER'), output_field=CharField(), ),
        ).values('key').annotate(avg=Avg('ul_bitrate'),
                                 min=Min('ul_bitrate'),
                                 max=Max('ul_bitrate'))

        start_date = self.kwargs.get('start')
        end_date = self.kwargs.get('end')
        network_type = self.kwargs.get('network_type', None)
        return queryset.filter(network_type__icontains=network_type, timestamp__gte=start_date,
                               timestamp__lte=end_date)

    # Down Link View for All Providers and Network Types


class DownLinkView(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Measurements.objects.annotate(key=Case(When(operatorname__icontains='wind', then=Value('WIND')),
                                                      When(operatorname__icontains='vodafone',
                                                           then=Value('VODAFONE')),
                                                      When(operatorname__icontains='cosmote',
                                                           then=Value('COSMOTE')),
                                                      default=Value('OTHER'), output_field=CharField(), ),
                                             ).values('key').annotate(avg=Avg('dl_bitrate'),
                                                                      min=Min('dl_bitrate'),
                                                                      max=Max('dl_bitrate'))
    serializer_class = GlobalSerializer

    def get_queryset(self):
        """ allow rest api to filter by network type """
        queryset = Measurements.objects.annotate(
            key=Case(When(operatorname__icontains='wind', then=Value('WIND')),
                     When(operatorname__icontains='vodafone',
                          then=Value('VODAFONE')),
                     When(operatorname__icontains='cosmote',
                          then=Value('COSMOTE')),
                     default=Value('OTHER'), output_field=CharField(), ),
        ).values('key').annotate(avg=Avg('dl_bitrate'),
                                 min=Min('dl_bitrate'),
                                 max=Max('dl_bitrate'))

        network_type = self.request.query_params.get('network_type', None)
        if network_type is not None:
            queryset = queryset.filter(network_type__icontains=network_type)
        return queryset

    # Down Link View for All Providers and Network Types with network type parameters


class DownLinkNetworkView(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Measurements.objects.annotate(key=Case(When(operatorname__icontains='wind', then=Value('WIND')),
                                                      When(operatorname__icontains='vodafone',
                                                           then=Value('VODAFONE')),
                                                      When(operatorname__icontains='cosmote',
                                                           then=Value('COSMOTE')),
                                                      default=Value('OTHER'), output_field=CharField(), ),
                                             ).values('key').annotate(avg=Avg('dl_bitrate'),
                                                                      min=Min('dl_bitrate'),
                                                                      max=Max('dl_bitrate'))
    serializer_class = GlobalSerializer

    def get_queryset(self):
        """ allow rest api to filter by network type """
        queryset = Measurements.objects.annotate(
            key=Case(When(operatorname__icontains='wind', then=Value('WIND')),
                     When(operatorname__icontains='vodafone',
                          then=Value('VODAFONE')),
                     When(operatorname__icontains='cosmote',
                          then=Value('COSMOTE')),
                     default=Value('OTHER'), output_field=CharField(), ),
        ).values('key').annotate(avg=Avg('dl_bitrate'),
                                 min=Min('dl_bitrate'),
                                 max=Max('dl_bitrate'))

        network_type = self.kwargs.get('network_type', None)
        return queryset.filter(network_type__icontains=network_type)

    # Down Link View for All Providers and Network Types with date range params


class DownLinkDateView(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Measurements.objects.annotate(key=Case(When(operatorname__icontains='wind', then=Value('WIND')),
                                                      When(operatorname__icontains='vodafone',
                                                           then=Value('VODAFONE')),
                                                      When(operatorname__icontains='cosmote',
                                                           then=Value('COSMOTE')),
                                                      default=Value('OTHER'), output_field=CharField(), ),
                                             ).values('key').annotate(avg=Avg('dl_bitrate'),
                                                                      min=Min('dl_bitrate'),
                                                                      max=Max('dl_bitrate'))
    serializer_class = GlobalSerializer

    def get_queryset(self):
        """ allow rest api to filter by timestamp """
        queryset = Measurements.objects.annotate(
            key=Case(When(operatorname__icontains='wind', then=Value('WIND')),
                     When(operatorname__icontains='vodafone',
                          then=Value('VODAFONE')),
                     When(operatorname__icontains='cosmote',
                          then=Value('COSMOTE')),
                     default=Value('OTHER'), output_field=CharField(), ),
        ).values('key').annotate(avg=Avg('dl_bitrate'),
                                 min=Min('dl_bitrate'),
                                 max=Max('dl_bitrate'))

        start_date = self.kwargs.get('start')
        end_date = self.kwargs.get('end')
        return queryset.filter(timestamp__gte=start_date, timestamp__lte=end_date)

    # Down Link View for All Providers and Network Types with date range
    # and Network Type params


class DownLinkDateNetworkView(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Measurements.objects.annotate(key=Case(When(operatorname__icontains='wind', then=Value('WIND')),
                                                      When(operatorname__icontains='vodafone',
                                                           then=Value('VODAFONE')),
                                                      When(operatorname__icontains='cosmote',
                                                           then=Value('COSMOTE')),
                                                      default=Value('OTHER'), output_field=CharField(), ),
                                             ).values('key').annotate(avg=Avg('dl_bitrate'),
                                                                      min=Min('dl_bitrate'),
                                                                      max=Max('dl_bitrate'))
    serializer_class = GlobalSerializer

    def get_queryset(self):
        """ allow rest api to filter by timestamp """
        queryset = Measurements.objects.annotate(
            key=Case(When(operatorname__icontains='wind', then=Value('WIND')),
                     When(operatorname__icontains='vodafone',
                          then=Value('VODAFONE')),
                     When(operatorname__icontains='cosmote',
                          then=Value('COSMOTE')),
                     default=Value('OTHER'), output_field=CharField(), ),
        ).values('key').annotate(avg=Avg('dl_bitrate'),
                                 min=Min('dl_bitrate'),
                                 max=Max('dl_bitrate'))

        start_date = self.kwargs.get('start')
        end_date = self.kwargs.get('end')
        network_type = self.kwargs.get('network_type', None)
        return queryset.filter(network_type__icontains=network_type, timestamp__gte=start_date,
                               timestamp__lte=end_date)

    # Network Type View (i.e 2G, 3G, 4G)


class NetworkTypeView(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Measurements.objects.annotate(key=Case(When(network_type__icontains='4g', then=Value('4G')),
                                                      When(network_type__icontains='3g',
                                                           then=Value('3G')),
                                                      When(network_type__icontains='2g',
                                                           then=Value('2G')),
                                                      default=Value('-'), output_field=CharField(), ),
                                             ).values('key').annotate(value=Count('network_type'))

    serializer_class = CountSerializer

    def get_queryset(self):
        """ allow rest api to filter by networkType """
        queryset = Measurements.objects.annotate(key=Case(When(network_type__icontains='4g', then=Value('4G')),
                                                          When(network_type__icontains='3g',
                                                               then=Value('3G')),
                                                          When(network_type__icontains='2g',
                                                               then=Value('2G')),
                                                          default=Value('-'), output_field=CharField(), ),
                                                 ).values('key').annotate(value=Count('network_type'))

        network_type = self.request.query_params.get('network_type', None)
        if network_type is not None:
            queryset = queryset.filter(key=network_type)
        return queryset

    # Operating System View (Mobile Version)



class OperatingSystemView(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Measurements.objects.values('versionname').annotate(value=Count('versionname'))

    serializer_class = OperatingSystemSerializer

    def get_queryset(self):
        """ allow rest api to filter by Mobile Version """
        queryset = Measurements.objects.values('versionname').annotate(value=Count('versionname'))

        versionname = self.request.query_params.get('versionname', None)
        if versionname is not None:
            queryset = queryset.filter(versionname=versionname)
        return queryset

    # Vendors View


class VendorsView(viewsets.ModelViewSet):
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication, BasicAuthentication)
    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Measurements.objects.values('devicemanufacturer').annotate(value=Count('devicemanufacturer'))

    serializer_class = VendorsSerializer

    def get_queryset(self):
        """ allow rest api to filter by Device Manufacturer """
        queryset = Measurements.objects.values('devicemanufacturer').annotate(value=Count('devicemanufacturer'))

        devicemanufacturer = self.request.query_params.get('devicemanufacturer', None)
        if devicemanufacturer is not None:
            queryset = queryset.filter(devicemanufacturer=devicemanufacturer)
        return queryset


class TablesListView(MultiTableMixin, TemplateView):
    template_name = 'mk/base.html'
    querysetMNOs = OperatorView.queryset
    querysetCamps = V2OfCampaigns.objects.all()
    querysetNet = NetworkTypeView.queryset
    tables = [
        MNOsTable(querysetMNOs, template_name='django_tables2/bootstrap-responsive.html'),
        CampaignsTable(querysetCamps, template_name='django_tables2/bootstrap-responsive.html'),
        NetworksTable(querysetNet, template_name='django_tables2/bootstrap-responsive.html'),
    ]

