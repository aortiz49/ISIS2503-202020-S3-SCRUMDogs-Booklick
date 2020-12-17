import django_filters
from django_filters import filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, viewsets

from content.models import Content, Interest
from django_filters import rest_framework as filters


class ContentSerializer(serializers.HyperlinkedModelSerializer):
    interests = serializers.PrimaryKeyRelatedField(queryset=Interest.objects.all(), many=True)

    class Meta:
        model = Content
        fields = ('id', 'title', 'relevanceScore', 'interests', 'type', 'url')


class InterestSerializer(serializers.HyperlinkedModelSerializer):
    relatedContent = ContentSerializer(many=True, read_only=True)

    class Meta:
        model = Interest
        fields = ('keyword', 'relatedContent')


class ListFilter(django_filters.Filter):
    def filter(self, qs, value):
        if value not in (None, ''):
            integers = [str(v) for v in value.split(',')]
            return qs.filter(**{'%s__%s' % (self.field_name, self.lookup_expr): integers})
        return qs


class ContentFilter(django_filters.FilterSet):
    ids = ListFilter(field_name="id", lookup_expr='in')

    class Meta:
        model = Content
        fields = ['ids']


