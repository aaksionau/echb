from .models import Comment
from django.forms import ModelForm
from django import forms


class NotAuthorizedCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Ваше имя', 'class': 'form__text'}),
            'email': forms.TextInput(attrs={'placeholder': 'Ваш Email', 'class': 'form__text'}),
            'body': forms.Textarea(attrs={'placeholder': 'Ваш комментарий', 'class': 'form__text', 'rows': 5})
        }
        labels = {
            'name': '',
            'email': '',
            'body': ''
        }


class AuthorizedCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)
        widgets = {
            'body': forms.Textarea(
                attrs={'placeholder': 'Ваш комментарий', 'class': 'form__text', 'rows': 5})
        }
        labels = {
            'body': ''
        }
