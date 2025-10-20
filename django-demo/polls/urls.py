from django.urls import path
from . import views

urlpatterns = [
    path('hello', views.hello_world),
    path('query_params', views.query_params),
    path('submit_form', views.submit_form),
    path('get_only', views.get_only_view),
    path('post_only', views.post_only_view),
    path('preview', views.preview_view, name='preview_view'),
    path('submit_form_view', views.submit_form_view, name='submit_form_view'),
    path('test_middleware', views.test_middleware, name='test_middleware'),
    path('trigger_error', views.trigger_error, name='trigger_error'),
]