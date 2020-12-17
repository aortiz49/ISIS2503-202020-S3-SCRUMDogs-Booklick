from django.db import models

# Create your models here.
from django.db import models
from django.utils.datetime_safe import datetime


class Interest(models.Model):
    keyword = models.CharField(max_length=50, primary_key=True)

    def __str__(self):
        return f'{self.keyword}'


class Content(models.Model):
    id = models.CharField(max_length=100, primary_key=True)
    relevanceScore = models.FloatField(null=True, blank= True, default=0)
    title = models.CharField(max_length= 200)
    interests = models.ManyToManyField(Interest,related_name ='relatedContent',  blank= True,)
    type = models.CharField(max_length= 50)
    url = models.CharField(max_length= 50)

    def __str__(self):
        return f'{self.id} - {self.title}'


class OnlineArticle(models.Model):
    description = models.CharField(max_length=500)
    author = models.CharField(max_length=30)
    date = models.DateTimeField(default=datetime.now, blank=True)
    url = models.CharField(max_length=200)
    id = models.OneToOneField(Content, on_delete=models.CASCADE, primary_key=True)


class Blog(models.Model):
    description = models.CharField(max_length=500)
    author = models.CharField(max_length=30)
    date = models.DateTimeField(default=datetime.now, blank=True)
    url = models.CharField(max_length=200)
    id = models.OneToOneField(Content, on_delete=models.CASCADE, primary_key=True)

class Video(models.Model):
    description = models.CharField(max_length=500)
    author = models.CharField(max_length=30)
    format = models.CharField(max_length=10)
    size = models.IntegerField()
    duration = models.IntegerField()
    date = models.DateTimeField(default=datetime.now, blank=True)
    url = models.CharField(max_length=200)
    id = models.OneToOneField(Content, on_delete=models.CASCADE, primary_key=True)

class Podcast(models.Model):
    description = models.CharField(max_length=500)
    author = models.CharField(max_length=30)
    format = models.CharField(max_length=10)
    size = models.IntegerField()
    duration = models.IntegerField()
    episode = models.IntegerField()
    date = models.DateTimeField(default=datetime.now, blank=True)
    url = models.CharField(max_length=200)
    id = models.OneToOneField(Content, on_delete=models.CASCADE, primary_key=True)
