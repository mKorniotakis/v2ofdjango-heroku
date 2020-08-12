from django.contrib.gis import admin
from django.apps import apps


# Register your models here.

# Auto register
def auto_register(model):
    # Get all fields from model, but exclude autocreated reverse relations
    field_list = [f.name for f in model._meta.get_fields() if f.auto_created == False]
    # Dynamically create ModelAdmin class and register it.
    my_admin = type('MyAdmin', (admin.ModelAdmin,),
                    {'list_display': field_list}
                    )
    my_gis_admin = type('MyGISAdmin', (admin.OSMGeoAdmin,),
                        {
                            'list_display': field_list,
                            'empty_value_display': 'empty'
                        }
                        )

    try:
        if (model._meta.model_name == 'measurements'):
            admin.site.register(model, my_gis_admin)
        else:
            if (model._meta.model_name == 'v2ofareas'):
                admin.site.register(model, my_gis_admin)
            else:
                if (model._meta.model_name == 'v2ofcollections'):
                    admin.site.register(model, my_gis_admin)
                else:
                    admin.site.register(model, my_admin)

    except AlreadyRegistered:
        # This model is already registered
        pass


for model in apps.get_app_config('myapp').get_models():
    auto_register(model)
