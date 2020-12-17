import requests
from django.http import JsonResponse

from rest_framework import viewsets
from rest_framework.parsers import JSONParser

from .serializers import ContentSerializer, InterestSerializer, ContentFilter
from content.models import Content, Interest


class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all().order_by('id')
    serializer_class = ContentSerializer

    def create(self, request, *args, **kwargs):

        data = JSONParser().parse(self.request)

        cont = data['id']
        keys = data['interests']

        url = 'http://ec2-18-207-139-221.compute-1.amazonaws.com:8000/updateInterests'
        dict = {"content": cont, "interests": keys}
        requests.post(url, json=dict)


        return JsonResponse(data, safe=False)



class InterestView(viewsets.ModelViewSet):
    queryset = Interest.objects.all()
    serializer_class = InterestSerializer


