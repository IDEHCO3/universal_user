from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('',
    url(r'^create/$', create_user, name='create'),
)