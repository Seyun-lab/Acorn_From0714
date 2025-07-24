# myapp/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('save/', views.save_data),
    path('list/', views.get_data),
]
