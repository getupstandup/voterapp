from django.contrib.gis import admin
from .models import *

class RepresentativeAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Representative._meta.get_fields() if f.name != 'id']
    search_fields = [f.name for f in Representative._meta.get_fields() if f.name != 'id']


class DistrictAdmin(admin.GeoModelAdmin):
    list_display = ['statefp', 'districtid']
    search_fields = ['statefp', 'districtid']


admin.site.register(District, DistrictAdmin)
admin.site.register(Voter)
admin.site.register(Issue)
admin.site.register(VoterResponse)
admin.site.register(Email)
admin.site.register(Representative, RepresentativeAdmin)
