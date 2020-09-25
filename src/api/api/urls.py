from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from rest_framework.urlpatterns import format_suffix_patterns
from django.views.static import serve
from api.views import home, SwaggerSchemaView


def generate_api_url_include(name):
    regex = r'^{}/'.format(name)
    namespace = 'doctor.{}'.format(name)
    if name == "docs":
        return url(regex, SwaggerSchemaView.as_view(), name=namespace)
    to_include = include('doctor.{}.urls'.format(name), namespace=namespace)
    return url(regex, to_include, name=namespace)


namespaces_to_include = [
    "docs",
    "user",
    "weight",
    "food_hydration",
    "motion",
    "sleep",
    "mind",
    "surrounding",
    "stop_challenge_choose",
    "alerts",
    "badges",
    "feedback",
    "video"
]


api_namespace_urls = [
    generate_api_url_include(name) for name in namespaces_to_include
]


urlpatterns = [
    url(r'^api/v1/', include(api_namespace_urls)),
]


urlpatterns = format_suffix_patterns(urlpatterns)


urlpatterns += [
    url(r'^_admin/', include(admin.site.urls)),
    url(r'^$', home, name='home'),
    url(r'^uploads/(.*)$', serve, {
        'document_root': settings.MEDIA_ROOT, 'show_indexes': True
        }),
]


try:
    urlpatterns += [
        url(r'^silk/', include('silk.urls', namespace='silk')),
    ]
except Exception as error:
    pass
