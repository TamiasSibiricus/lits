from django.contrib import admin
from .models import (Reporter, Tag, License, Article,
                     Comment)

class LicenseInline(admin.TabularInline):
    model = License

@admin.register(Reporter)
class ReporterAdmin(admin.ModelAdmin):
    inlines = [
        LicenseInline,
    ]
    list_display = ('id', 'firstname', 'lastname', 'license',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_with_reporter', 'created_at', 'published_at',)
    list_select_related = ('reporter',)

    @admin.display(description='Title with reporter')
    def title_with_reporter(self, obj):
        return ("%s (%s %s)" % (obj.title, obj.reporter.firstname, obj.reporter.lastname))

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user_or_username', 'content', 'aproved')
    list_editable = ['aproved']
    list_select_related = ('user',)

    @admin.display(description='Title with reporter')
    def user_or_username(self, obj):
        return obj.username or obj.user

