from django.urls import path, re_path
from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token, refresh_jwt_token, verify_jwt_token
from allauth.account.views import LoginView

from myapp.views import *

urlpatterns = [
    url(r'^api-token-auth/', obtain_jwt_token),
    url(r'^api-token-refresh/', refresh_jwt_token),
    url(r'^api-token-verify/', verify_jwt_token),

    # API Documentation url
    url(r'^apiDoc/', schema_view),

    # All Auth URLS
    path('account/', include('allauth.urls')),
    path('account/avatar/', include('avatar.urls')),
    path('account/profile/', include('userprofiles.urls')),

    url(r'^$', LoginView.as_view(), name='login'),

    url(r'^home/', HomePageView.as_view(), name='home'),

    # Display Openlayers map
    url(r'^map/', MapPageView.as_view(), name='map'),

    # Display data
    url(r'^operators/', OperatorView.as_view({'get': 'list'})),

    # Count all providers
    url(r'^providers/', CountView.as_view({'get': 'list'})),

    # Statistic Charts
    path('levelStats/', StatisticsView.as_view({'get': 'list'})),

    # Statistic Charts
    re_path(r'^levelStats/(?P<network_type>\w+)/$', StatisticsNetworkView.as_view({'get': 'list'})),

    # Statistics Charts with date range params
    re_path(r'^levelStats/(?P<start>[\w\-\.]+) - (?P<end>[\w\-\.]+)/$',
            StatisticsDateView.as_view({'get': 'list'})),

    # Statistics Charts with date range and network type params
    re_path(r'^levelStats/(?P<start>[\w\-\.]+) - (?P<end>[\w\-\.]+)/(?P<network_type>\w+)/$',
            StatisticsDateNetworkView.as_view({'get': 'list'})),

    # Up link Bit Rate for each Provider
    path('uplinkStats/', UpLinkView.as_view({'get': 'list'})),

    # Up link Bit Rate with network type params
    re_path(r'^uplinkStats/(?P<network_type>\w+)/$', UpLinkNetworkView.as_view({'get': 'list'})),

    # Up link Bit Rate with date range params
    re_path(r'^uplinkStats/(?P<start>[\w\-\.]+) - (?P<end>[\w\-\.]+)/$',
            UpLinkDateView.as_view({'get': 'list'})),

    # Up link Bit Rate with date range and network type params
    re_path(r'^uplinkStats/(?P<start>[\w\-\.]+) - (?P<end>[\w\-\.]+)/(?P<network_type>\w+)/$',
            UpLinkDateNetworkView.as_view({'get': 'list'})),

    # Down link Bit Rate for each Provider
    path('downlinkStats/', DownLinkView.as_view({'get': 'list'})),

    # Down link Bit Rate with network type params
    re_path(r'^downlinkStats/(?P<network_type>\w+)/$', DownLinkNetworkView.as_view({'get': 'list'})),

    # Down link Bit Rate with date range params
    re_path(r'^downlinkStats/(?P<start>[\w\-\.]+) - (?P<end>[\w\-\.]+)/$',
            DownLinkDateView.as_view({'get': 'list'})),

    # Down link Bit Rate with date range and network type params
    re_path(r'^downlinkStats/(?P<start>[\w\-\.]+) - (?P<end>[\w\-\.]+)/(?P<network_type>\w+)/$',
            DownLinkDateNetworkView.as_view({'get': 'list'})),

    # Count Operators by Network Type
    url(r'^networks/', NetworkTypeView.as_view({'get': 'list'})),

    # Find Mobile Version
    url(r'^osStats/', OperatingSystemView.as_view({'get': 'list'})),

    # Vendors
    url(r'^vendorStats/', VendorsView.as_view({'get': 'list'})),

    # Display data from Measurements legacyDB
    url(r'^measurements/', MeasurementsView.as_view()),

    path('campaigns/', CampaignsListView.as_view(), name='campaigns'),
    re_path(r'^campaigns/(?P<pk>\d+)$', CampaignsDetailView.as_view(), name='campaign-detail'),

    # geoJSON layer as example
    url(r'^data.geojson$', geojsonFeed, name='data'),

    #path('mk/', MKPageView.as_view(), name='dashboard'),
    re_path(r'^mk/', TablesListView.as_view(), name='dashboard'),
]
