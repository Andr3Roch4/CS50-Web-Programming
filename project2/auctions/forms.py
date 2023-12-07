from django import forms
from .models import Categories

class ListingsForm(forms.Form):
    name = forms.CharField(max_length=64, label="Name your listing:", required=True)
    startingbid = forms.IntegerField(label="Starting price in dollars:", min_value=1, required=True)
    description = forms.CharField(max_length=400, label="Description:", widget=forms.Textarea)
    image = forms.URLField(max_length=200, label="Link an image URL:")

class CategoriesForm(forms.Form):
    category = forms.ChoiceField(choices=Categories.categories, required=True, label="Select category:")

class CommentForm(forms.Form):
    comment = forms.CharField(max_length=200, label="Add your comment:", widget=forms.Textarea)
