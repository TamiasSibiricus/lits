"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from myproject import views
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from myproject import views_api

# REST routing here
router = routers.DefaultRouter()
router.register(r'articles', views_api.ArticleViewSet)
router.register(r'reporters', views_api.ReporterViewSet)
router.register(r'tags', views_api.TagViewSet)
router.register(r'users', views_api.UserViewSet)
router.register(r'groups', views_api.GroupViewSet)

# generic views
urlpatterns = [
    path('admin/', admin.site.urls),
    # Wire up our API using automatic URL routing.
    # Additionally, we include login URLs for the browsable API.
    path('api/', include(router.urls)),
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/export/articles/', views_api.ArticlesExportView.as_view(), name='articles_export'),
    #path('api/export/articles/', views_api.articles_export, name='articles_export'),
    # regular html
    path('', views.homepage, name='homepage'),
    path('articles/<str:slug>/', views.ArticleView.as_view(), name='article'),
    path('articles/<str:slug>/comment', views.add_comment, name='article_comment'),
    path('tag/<str:slug>/', views.TagView.as_view(), name='tag'),
    path('reporter/<str:slug>/', views.ReporterView.as_view(), name='reporter'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', views.register, name="account_register"),
    path('accounts/profile/', views.profile, name="account_profile"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
