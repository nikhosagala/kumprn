# Create your views here.

from rest_framework import generics

from news.models import Tag
from news.serializers import TagSerializer


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


class NewsView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):
    def get(self, request, *args, **kwargs):
        pass

    def post(self, request, *args, **kwargs):
        pass

    def put(self, request, *args, **kwargs):
        pass

    def delete(self, request, *args, **kwargs):
        pass
