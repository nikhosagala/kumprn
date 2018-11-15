# Create your views here.

from rest_framework import generics

from news.models import Tag, News
from news.serializers import TagSerializer, NewsSerializer


class TagList(generics.ListCreateAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects.all()

    def get_serializer_context(self):
        return {
            'request': self.request
        }


class TagDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TagSerializer
    queryset = Tag.objects
    lookup_field = 'slug'

    def get_serializer_context(self):
        return {
            'request': self.request
        }


class NewsList(generics.ListCreateAPIView):
    serializer_class = NewsSerializer
    queryset = News.objects.filter(is_active=True)

    def get_serializer_context(self):
        return {
            'request': self.request
        }


class NewsDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = NewsSerializer
    queryset = News.objects
    lookup_field = 'slug'

    def get_serializer_context(self):
        return {
            'request': self.request
        }

    def perform_destroy(self, instance):
        instance.is_active = False
        instance.save()
