# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from .models import Content, Interest, OnlineArticle, Blog, Video, Podcast, Content


admin.site.register(OnlineArticle)
admin.site.register(Blog)
admin.site.register(Video)
admin.site.register(Podcast)
admin.site.register(Interest)
admin.site.register(Content)

