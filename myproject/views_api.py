from django.db import transaction
from django.contrib.auth.models import User, Group
from django.shortcuts import get_object_or_404
from rest_framework import status, viewsets, permissions, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import Tag, Article, Reporter
from .serializers import (UserSerializer, GroupSerializer, ReporterSerializer,
                         TagSerializer, ArticleSerializer, ArticleCreateUpdateSerializer)


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
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
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
