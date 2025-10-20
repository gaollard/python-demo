from django.urls import path
from . import views

urlpatterns = [
    path('hello', views.hello_world),
    path('query_params', views.query_params),
    path('submit_form', views.submit_form),
    path('get_only', views.get_only_view),
    path('post_only', views.post_only_view),
    path('get_post', views.get_post_view),
]