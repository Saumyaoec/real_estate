from django.urls import path
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('properties-create/', PropertyCreateAPIView.as_view(), name='property-create'),
    path('properties-list/', PropertyListAPIView.as_view(), name='property-list'),
    path('properties/<int:property_id>/units/', UnitListCreateAPIView.as_view(), name='unit-list-create'),
    path('properties/<int:property_id>/units/<int:unit_id>/', UnitDetailAPIView.as_view(), name='unit-detail'),
   
]