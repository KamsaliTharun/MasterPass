from django.urls import path
from visit_places.views import *

urlpatterns = [
    path("", home, name="home"),
]
