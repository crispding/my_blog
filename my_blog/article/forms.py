from django import forms
from .models import ArticlePost


class ArticePostForm(forms.ModelForm):
    class Meta:
        model = ArticlePost
        fields = ('title', 'excerpt', 'tags', 'body')
