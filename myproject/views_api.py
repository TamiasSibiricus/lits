from django.db import transaction
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions, filters
from rest_framework.decorators import (api_view, permission_classes,
                                        renderer_classes)
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_csv.renderers import CSVRenderer
from django_filters.rest_framework import DjangoFilterBackend
from rest_access_policy import AccessViewSetMixin


from .models import Tag, Article, Reporter
from .serializers import (UserSerializer, GroupSerializer, ReporterSerializer,
                         TagSerializer, ArticleSerializer, ArticleCreateUpdateSerializer)
from .policies import ArticleAccessPolicy, AdminOnlyAccessPolicy


class MultiSerializerViewSetMixin(object):
    def get_serializer_class(self):
        try:
            return self.serializer_action_classes[self.action]
        except (KeyError, AttributeError):
            return super(MultiSerializerViewSetMixin, self).get_serializer_class()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    search_fields = ['^username']
    ordering_fields = ['date_joined', 'last_login']
    ordering = ['-date_joined']

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name']

class ReporterViewSet(viewsets.ModelViewSet):
    queryset = Reporter.objects.all()
    serializer_class = ReporterSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filterset_fields = ['firstname', 'lastname']

class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all().order_by('name')
    serializer_class = TagSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class ArticleViewSet(MultiSerializerViewSetMixin, viewsets.ModelViewSet):
    queryset = Article.objects.all().order_by('-published_at')
    serializer_class = ArticleSerializer
    serializer_action_classes = {
        'create': ArticleCreateUpdateSerializer,
        'update': ArticleCreateUpdateSerializer,
    }
    permission_classes = [ArticleAccessPolicy]
    # NOTE: access_policy coud used only with AccessViewSetMixin
    #access_policy = ArticleAccessPolicy
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter
    ]
    filterset_fields = ['slug']
    search_fields = ['title']
    ordering_fields = ['published_at']
    ordering = ['-published_at']

    @transaction.atomic
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        pk = serializer.data.get('id')
        if pk:
            instance = get_object_or_404(Article, pk=pk)
            serializer = ArticleSerializer(instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @transaction.atomic
    def update(self, request, pk=None):
        instance = get_object_or_404(Article, pk=pk)
        serializer = self.get_serializer(instance, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        headers = self.get_success_headers(serializer.data)
        instance = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)

    @transaction.atomic
    def partial_update(self, request, pk=None):
        instance = get_object_or_404(Article, pk=pk)
        serializer = self.get_serializer(instance, data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer, partial=True)
        headers = self.get_success_headers(serializer.data)
        instance = get_object_or_404(Article, pk=pk)
        serializer = ArticleSerializer(instance, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK, headers=headers)



class ArticleCSVRenderer(CSVRenderer):
    header = ['title', 'url', 'headline']


class ArticlesExportView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    access_policy = AdminOnlyAccessPolicy
    #renderer_classes = (ArticleCSVRenderer,)

    def get(self, request, format=None):
        response = [ArticleSerializer(instance, context={'request': request}).data for instance in Article.objects.all()]
        return Response(response)


@api_view(['GET'])
@permission_classes((AdminOnlyAccessPolicy,))
#@renderer_classes((ArticleCSVRenderer,))
def articles_export(request):
    '''
    articles = Article.objects.all()
    response = [{'title': article.title,
        'slug': article.slug,
        'headline': article.headline}
        for article in articles]
    '''
    response = [ArticleSerializer(instance, context={'request': request}).data for instance in Article.objects.all()]
    return Response(response)
