import markdown
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.html import strip_tags
# Django-taggit
from taggit.managers import TaggableManager


# Create your models here.
class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    body = models.TextField()
    excerpt = models.CharField(max_length=200, blank=True)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(auto_now=True)
    total_views = models.PositiveIntegerField(default=0)
    # 文章标签
    tags = TaggableManager(blank=True)

    class Meta:
        ordering = ('-created',)

    def save(self, *args, **kwargs):
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
        ])
        self.excerpt = strip_tags(md.convert(self.body))[:100]
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
