from django.conf.urls import patterns, url
from authentication import views
from django.contrib.auth.views import login
from django.contrib.auth.views import logout
from .views import authetication
from .views import WhoAmI

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
    url(r'^authentication/signin/?$', 'rest_framework_jwt.views.obtain_jwt_token', name='signin'),
    url(r'^authentication/token-refresh/?$', 'rest_framework_jwt.views.refresh_jwt_token', name='tokenRefresh'),
    url(r'^authentication/token-verify/?$', 'rest_framework_jwt.views.verify_jwt_token'),
    url(r'^authentication/me/?$', WhoAmI.as_view(), name='me'),
    url(r'^authentication/index/?$', authetication, name='index'),
    url(r'^$', authetication, name='initial'),
)

urlpatterns = format_suffix_patterns(urlpatterns)