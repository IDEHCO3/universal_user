from django.conf.urls import patterns, url
from .views import *

urlpatterns = patterns('',
    url(r'^$', UserList.as_view(), name='list'),
    url(r'^facebook/?$', UserFacebook.as_view(), name='facebook'),
    url(r'^(?P<pk>\d+)/?$', UserDetail.as_view(), name='detail'),
    url(r'^(?P<user_uuid>[\d\-\w]+)/?$', UserDetailUUID.as_view(), name='detail'),
)