from django.contrib.auth.models import User, Group
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import UserProfile, Article, Reporter, Tag


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['firstname', 'lastname', 'birth_date']


class GroupListField(serializers.RelatedField):
    def get_queryset(self):
        return Group.objects.all()

    def to_representation(self, value):
        return value.name

    def to_internal_value(self, data):
        return data


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = UserProfileSerializer()
    password = serializers.CharField(
        max_length=60,
        trim_whitespace=True,
        required=True,
        write_only=True,
        help_text=_(
            "Required. 128 characters or fewer. Letters and digits only."
        )
    )
    email = serializers.EmailField()
    groups = GroupListField(many=True)

    class Meta:
        model = User
        fields = ['url', 'username', 'password', 'email', 'groups', 'profile']

class ReporterSerializer(serializers.HyperlinkedModelSerializer):
    articles = serializers.HyperlinkedRelatedField(
        many=True,
        read_only=True,
        view_name='article-detail'
    )
    class Meta:
        model = Reporter
        fields = ['url', 'firstname', 'lastname', 'articles']


class TagListField(serializers.RelatedField):
    def get_queryset(self):
        return Tag.objects.all()

    def to_representation(self, value):
        return value.name

    def to_internal_value(self, data):
        return data



class ArticleSerializer(serializers.HyperlinkedModelSerializer):
    tags = TagListField(many=True)
    reporter = ReporterSerializer(many=False)
    published_at = serializers.DateTimeField()

    class Meta:
        model = Article
        fields = ['url', 'title', 'slug', 'headline', 'content', 'published_at', 'tags', 'reporter']


class TagSerializer(serializers.HyperlinkedModelSerializer):
    # TODO: ManyToMany does not work. Solution needed
    #articles = serializers.HyperlinkedRelatedField(
    #    many=True,
    #    read_only=True,
    #    view_name='article-detail'
    #)
    articles = serializers.SerializerMethodField()
    class Meta:
        model = Tag
        fields = ['url', 'name', 'articles']

    def get_articles(self, obj):
        articles = Article.objects.prefetch_related(
                'tags'
            ).filter(tags__name=obj.name)
        return [ArticleSerializer(article, context={'request': self.context['request']}).data.get('url') for article in articles]

