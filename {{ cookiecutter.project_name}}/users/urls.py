"""Users URL Configuration."""
from django.urls import include, path

urlpatterns = [
    {% if cookiecutter.app_type == 'django rest framework with dj-rest-auth' -%}
    path("register/", include("dj_rest_auth.registration.urls")),
    path("", include("dj_rest_auth.urls")),
    {%- endif %}
]
