from django.urls import path
from . import views

urlpatterns = [
    path('hello', views.hello_world),
    path('query_params', views.query_params),
]