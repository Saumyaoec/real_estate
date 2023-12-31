from django.urls import path
from . import views

urlpatterns = [
    path('tenants/', views.TenantListCreateAPIView.as_view(), name='tenant-list-create'),
    path('tenant-assignments/', views.TenantAssignmentListCreateAPIView.as_view(), name='tenant-assignment-list-create'),
]
