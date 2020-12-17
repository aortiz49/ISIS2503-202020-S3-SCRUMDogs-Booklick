from django.conf.urls import url, include

from .views import *

urlpatterns =[
    url(r'^interests/$', interests),
    url(r'^interestsDetails/(?P<pk>\w+)$', interestsDetail),
    url(r'^contentByKey/(?P<pk>\w+)$', contentByKey),
    url(r'^updateInterests$', updateInterests),
]