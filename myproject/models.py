from django.db import models

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
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    headline = models.CharField(max_length=256)
    content = models.TextField()
    pub_date = models.DateField()

    def __str__(self):
        return self.headline
