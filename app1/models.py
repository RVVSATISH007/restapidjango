from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    url = models.URLField(unique=True)
    source = models.CharField(max_length=100)
    published_at = models.DateTimeField()

    def __str__(self):
        return self.title
