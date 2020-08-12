import django_tables2 as tables
from django_tables2 import A
from .models import V2OfCampaigns, Measurements


class CampaignsTable(tables.Table):
    class Meta:
        model = V2OfCampaigns
        attrs = {"class": "table table-bordered table-hover", "id": "bootstrap-table"}
        sequence = ('id', 'name', '...')
        row_attrs = {
            'data-formatter': "operateFormatter",
            'data-events': "operateEvents"
        }

        empty_text = "There are no campaigns matching the search criteria..."


class MNOsTable(tables.Table):
    class Meta:
        model = Measurements
        attrs = {"class": "table table-bordered table-hover", "id": "bootstrap-table"}
        row_attrs = {
            'data-formatter': "operateFormatter",
            'data-events': "operateEvents"
        }


class NetworksTable(tables.Table):
        class Meta:
            model = Measurements
            attrs = {"class": "table table-bordered table-hover", "id": "bootstrap-table"}
            row_attrs = {
                 'data-formatter': "operateFormatter",
                 'data-events': "operateEvents"
            }
            template_name = 'django_tables2/bootstrap.html'