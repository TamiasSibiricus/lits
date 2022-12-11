import re
from django.shortcuts import get_object_or_404
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from ..models import Article, Reporter, Tag
from ..validators import alpha_only, AlphaOnlyValidator

class ReporterSerializer(serializers.HyperlinkedModelSerializer):
    articles = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='article-detail'
    )
    class Meta:
        model = Reporter
        fields = ['url', 'id', 'firstname', 'lastname', 'articles']


class TagListField(serializers.RelatedField):
    def get_queryset(self):
        return Tag.objects.all()

    def to_representation(self, value):
        return value.name

    def to_internal_value(self, data):
        return get_object_or_404(Tag, name=data)


class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    title = serializers.CharField(max_length=200)
    slug = serializers.SlugField(max_length=200)
    #slug = serializers.SlugField(
    #    max_length=200,
    #    validators=[
    #        alpha_only,
    #        #AlphaOnlyValidator('something'),
    #        UniqueValidator(queryset=Article.objects.all())
    #    ]
    #)
    tags = TagListField(many=True)
    reporter = ReporterSerializer(many=False)
    published_at = serializers.DateTimeField()

    class Meta:
        model = Article
        fields = ['url', 'id', 'title', 'slug', 'headline', 'content', 'published_at', 'tags', 'reporter']

    def validate_slug(self, value):
        slug_re = re.compile(r'^[-a-zA-Z_]+$')
        if not slug_re.match(value):
            raise serializers.ValidationError('Not an alphabet slug. Digits not allowed by field validation')
        return value

class ArticleCreateUpdateSerializer(ArticleSerializer):
    reporter = serializers.PrimaryKeyRelatedField(
            queryset=Reporter.objects.all(),
            many=False,
        )

    def create(self, validated_data):
        # Extract relations which should processed manually here
        tags = validated_data.pop('tags', [])
        # Create article instance
        instance = Article.objects.create(**validated_data)
        # Set relations many-to-many manually
        # They could be set only if instance already exists
        if tags:
            instance.tags.set(tags)
        # Save changes
        instance.save()
        return instance
        #response_serializer = ArticleSerializer(article, context={'request': self.context['request']})
        #print(response_serializer.data)
        #return response_serializer

    def update(self, instance, validated_data):
        # Extract relations which should processed manually here
        tags = validated_data.pop('tags', [])
        # Update article instance
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        # Set another list of tags
        if tags:
            instance.tags.set(tags)
        # Save changes
        instance.save()
        return instance



class TagSerializer(serializers.HyperlinkedModelSerializer):
    articles = serializers.SerializerMethodField()
    class Meta:
        model = Tag
        fields = ['url', 'id', 'name', 'articles']

    def get_articles(self, obj):
        articles = Article.objects.prefetch_related(
                'tags'
            ).filter(tags__name=obj.name)
        return [ArticleSerializer(article, context={'request': self.context['request']}).data.get('url') for article in articles]

