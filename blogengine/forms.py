from django import forms
from .models import *
from django.core.exceptions import ValidationError


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['tag_name', 'slug']
        labels = {
            'tag_name': 'Tag',
        }
        widgets = {
            'tag_name': forms.TextInput(attrs={'class': "form-control"}),
            'slug': forms.TextInput(attrs={'class': "form-control"}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug']
        if new_slug == 'create':
            raise ValidationError("Slug can't be 'create'")
        return new_slug


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'body', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': "form-control"}),
            'slug': forms.TextInput(attrs={'class': "form-control"}),
            'body': forms.Textarea(attrs={'class': "form-control"}),
            'tags': forms.SelectMultiple(attrs={'class': "form-control"}),
        }

    def clean_slug(self):
        new_slug = self.cleaned_data['slug']
        if new_slug == 'create':
            raise ValidationError("Slug can't be 'create'")
        return new_slug


