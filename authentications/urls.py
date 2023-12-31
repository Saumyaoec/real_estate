from django.urls import path
from django.views.generic import TemplateView
from .views import *

urlpatterns = [
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path("register/", SignupAPI.as_view(), name="register"),
    path("login/", LoginAPI.as_view(), name="login"),
    path('dashboard/', TemplateView.as_view(template_name='dashboard.html'), name='dashboard'),
]