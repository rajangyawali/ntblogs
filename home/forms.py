from django import forms
from . import models

from . models import BlogPost

class ContactForm(forms.Form):
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

class SubscriberForm(forms.Form):
    subscriber = forms.EmailField(required=True)

# class BlogPostForm(forms.Form):
#     class Meta:
#         model = BlogPost
#         fields = ['title', 'description', 'featured', 'image', 'category', 'author']
    
#     title = forms.CharField(required=True)
#     description = forms.CharField(widget=forms.Textarea, required=True)
#     featured = forms.ChoiceField(required=True, choices=models.FEATURED_OPTIONS, de)
#     image = forms.ImageField(required=True)
#     category = forms.ChoiceField(required=True, choices=models.CATEGORY_OPTIONS)
#     author = forms.ChoiceField(required=True)
    
