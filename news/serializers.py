from rest_framework import serializers

from news.models import Tag, News


class TagSerializer(serializers.ModelSerializer):
    href = serializers.HyperlinkedIdentityField(view_name='news:tag-detail', lookup_field='slug')

    class Meta:
        model = Tag
        fields = ('title', 'slug', 'href',)


class NewsSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = News
        fields = ('title', 'slug', 'tags')
