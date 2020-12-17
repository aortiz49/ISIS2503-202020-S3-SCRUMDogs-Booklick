from django.http import JsonResponse
from pymongo import MongoClient
import datetime
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.parsers import JSONParser
from django.conf import settings
from bson.objectid import ObjectId

from django.shortcuts import render
import requests

# Create your views here.


@api_view(["GET", "POST"])
def interests(request):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    interests = db['interests']
    if request.method == "GET":
        result = []
        data = interests.find({})
        for dto in data:
            jsonData = {
                "interest": dto['interest'],
                'content': dto['content']
            }
            result.append(jsonData)
        client.close()
        return JsonResponse(result, safe=False)

    if request.method == 'POST':
        data = JSONParser().parse(request)
        result = interests.insert(data)
        respo = {
            "MongoObjectID": str(result),
            "Message": "nuevo objeto en la base de datos"
        }
        client.close()
        return JsonResponse(respo, safe=False)


@api_view(["GET", "POST"])
def interestsDetail(request, pk):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    interests = db['interests']
    if request.method == "GET":
        data = interests.find({'_id': ObjectId(pk)})
        result = []
        for dto in data:
            jsonData = {
                'id': str(dto['_id']),
                "interest": dto['interest'],
                'content': dto['content']
            }
            result.append(jsonData)
        client.close()
        return JsonResponse(result[0], safe=False)
    if request.method == "POST":
        data = JSONParser().parse(request)
        result = interests.update(
            {'_id': ObjectId(pk)},
            {'$push': {'content': data}}
        )
        respo = {
            "MongoObjectID": str(result),
            "Message": "nuevo objeto en la base de datos"
        }
        client.close()
        return JsonResponse(respo, safe=False)


@api_view(["GET"])
def contentByKey(request, pk):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    interests = db['interests']

    res = []
    if request.method == "GET":
        data = interests.find({'interest': pk})
        result = []
        for dto in data:
            jsonData = {
                "interest": dto['interest'],
                'content': dto['content'],
            }
            result.append(jsonData)
            res = result[0]
        client.close()



        return JsonResponse(res, safe=False)

@api_view(["POST"])
def updateInterests(request):
    client = MongoClient(settings.MONGO_CLI)
    db = client.monitoring_db
    interests = db['interests']

    if request.method == "POST":
        data = JSONParser().parse(request)

        cont = data['content']
        keys = data['interests']

        for key in keys:
            interests.insert({"interest": key, "content": []})

        res = ""
        for key in keys:
          result = interests.update({'interest': key}, {'$push': {'content':  {"id": cont}}})
          res += str(result)

        respo = {
            "MongoObjectID": res,
            "Message": "objeto modificado la base de datos"
        }
        client.close()
        return JsonResponse(respo, safe=False)
