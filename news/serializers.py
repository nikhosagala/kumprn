from rest_framework import serializers

from news.models import Tag, News


class TagSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False)
    href = serializers.HyperlinkedIdentityField(view_name='news:tag-detail', lookup_field='slug')

    class Meta:
        model = Tag
        fields = ('title', 'slug', 'href',)


class NewsSerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(required=False)
    tags = TagSerializer(many=True)
    href = serializers.HyperlinkedIdentityField(view_name='news:news-detail', lookup_field='slug')

    def create(self, validated_data):
        tags = validated_data.pop('tags')
        news = News.objects.create(**validated_data)
        for tag_post in tags:
            tag, created = Tag.objects.get_or_create(title=tag_post.get('title'))
            news.tags.add(tag)
        news.save()
        return news

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags')
        for item in validated_data:
            if News._meta.get_field(item):
                setattr(instance, item, validated_data[item])
        for tag in instance.tags.all():
            instance.tags.remove(tag)
        for tag_update in tags:
            tag, created = Tag.objects.get_or_create(title=tag_update.get('title'))
            instance.tags.add(tag)
        instance.save()
        return instance

    class Meta:
        model = News
        fields = ('title', 'slug', 'status', 'tags', 'href')
