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
from django.urls import path
from myproject import views 
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('articles/<int:article_id>/', views.article, name='article')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

'''
# generic views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.IndexView.as_view(), name='index'),
    path('articles/<int:pk>/', views.ArticleView.as_view(), name='article_by_pk'),
    path('articles/<str:slug>/', views.ArticleView.as_view(), name='article_by_slug')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
'''
