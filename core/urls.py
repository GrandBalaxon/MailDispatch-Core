from django.urls import path
from .views import *
from .apps import CoreConfig

app_name = CoreConfig.name

urlpatterns = [
    path('', HomePageView.as_view(), name="home"),
]
