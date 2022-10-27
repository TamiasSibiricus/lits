from django.contrib import admin
from .models import (Reporter, Tag, License, Article,
                     Comment)


@admin.register(Reporter)
class ReporterAdmin(admin.ModelAdmin):
    list_display = ('id', 'firstname', 'lastname', 'license',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    pass

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'published_at',)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass

