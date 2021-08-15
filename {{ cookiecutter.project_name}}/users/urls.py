"""Users URL Configuration."""
from django.urls import include, path
{% if cookiecutter.app_type == 'django rest framework with firebase auth' -%}from .views import FireBaseAuthAPI{%- endif %}

urlpatterns = [
    {% if cookiecutter.app_type == 'django rest framework with dj-rest-auth' -%}
    path("register/", include("dj_rest_auth.registration.urls")),
    path("", include("dj_rest_auth.urls")),
    {%- endif %}
    {% if cookiecutter.app_type == 'django rest framework with firebase auth' -%}path('firebase/auth/', FireBaseAuthAPI.as_view(), name='firebase_auth'),{%- endif %}
]
