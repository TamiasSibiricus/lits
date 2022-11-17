from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='profile'
    )
    firstname = models.CharField(max_length=70, default='')
    lastname = models.CharField(max_length=70, default='')
    birth_date = models.DateField()

class Reporter(models.Model):
    firstname = models.CharField(max_length=70, default='')
    lastname = models.CharField(max_length=70, default='')

    def __str__(self):
        return f"{self.firstname} {self.lastname}"

class License(models.Model):
    number = models.CharField(max_length=200)
    reporter = models.OneToOneField(Reporter, on_delete=models.CASCADE)

    def __str__(self):
        return self.number

class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Article(models.Model):
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE, related_name='articles')
    tags = models.ManyToManyField(Tag, related_name='tags')
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    headline = models.CharField(max_length=256, null=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField()

    def __str__(self):
        return self.headline

class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    username = models.CharField(max_length=200, blank=True, null=True)
    content = models.TextField()
    aproved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        # WARNING! After permission add or change makemigration and migrate required
        permissions = (("can_comment", "Can leave comment for article"),)

    def __str__(self):
        return self.content
