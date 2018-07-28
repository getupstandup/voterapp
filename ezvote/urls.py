from django.contrib.gis import admin
from django.urls import include, path

from voter.views import *


urlpatterns = [
    path('admin/', admin.site.urls),
    path("", index, name="index"),
    path("question-confirm", question_confirm, name="question_confirm"),
    path("address-confirm", address_confirm, name="address_confirm"),
    path("chart-data", chart_data, name="chart_data"),
    path("save-email", save_email, name="save_email"),
]
