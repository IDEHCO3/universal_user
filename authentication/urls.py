from django.conf.urls import patterns, url
from authentication import views
from django.contrib.auth.views import login
from django.contrib.auth.views import logout
from .views import authetication
from .views import WhoAmI

from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = patterns('',
    url(r'^signin', 'rest_framework_jwt.views.obtain_jwt_token', name='signin'),
    url(r'^token-refresh', 'rest_framework_jwt.views.refresh_jwt_token', name='tokenRefresh'),
    url(r'^token-verify', 'rest_framework_jwt.views.verify_jwt_token'),
    url(r'^me$', WhoAmI.as_view(), name='me'),
    url(r'^index$', authetication, name='index'),
)

urlpatterns = format_suffix_patterns(urlpatterns)