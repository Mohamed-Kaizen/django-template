"""{{cookiecutter.project_name}} URL Configuration."""
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = i18n_patterns(
    path(f"{settings.ADMIN_URL}", admin.site.urls),
    path(
        ".well-known/security.txt",
        TemplateView.as_view(template_name="security.txt", content_type="text/plain",),
    ),
    path(
        "robots.txt",
        TemplateView.as_view(template_name="robots.txt", content_type="text/plain",),
    ),
    path("api/users/", include("users.urls")),
    prefix_default_language=False
)

if settings.DEBUG:
    import debug_toolbar
    from django.conf.urls.static import static

    {% if cookiecutter.app_type == 'django rest framework with dj-rest-auth' or cookiecutter.app_type == "django rest framework with firebase auth"  -%}
    from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
    {%- endif %}

    urlpatterns += [
        {% if cookiecutter.app_type == 'django rest framework with dj-rest-auth' or cookiecutter.app_type == "django rest framework with firebase auth" -%}
        path('schema/', SpectacularAPIView.as_view(), name='schema'),
        path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
        path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
        {%- endif %}
        path("__debug__/", include(debug_toolbar.urls))
    ] + static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
