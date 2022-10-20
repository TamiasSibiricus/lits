from django.contrib import admin
from .models import Reporter, Tag, License, Article

@admin.register(Reporter)
class ReporterAdmin(admin.ModelAdmin):
    pass

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass

@admin.register(License)
class LicenseAdmin(admin.ModelAdmin):
    pass

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    pass
