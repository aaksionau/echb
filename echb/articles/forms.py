from .models import Comment
from django.forms import ModelForm, TextInput, Textarea


class NotAuthorizedCommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')
        widgets = {
            'name': TextInput(
                attrs={'placeholder': 'Ваше имя', 'class': 'form__text'}),
            'email': TextInput(
                attrs={'placeholder': 'Ваш Email', 'class': 'form__text'}),
            'body': Textarea(
                attrs={'placeholder': 'Вашe cообщение', 'class': 'form__text', 'rows': 5})
        },
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
            'body': Textarea(
                attrs={'placeholder': 'Вашe cообщение', 'class': 'form__text', 'rows': 5})
        }
        labels = {
            'body': ''
        }
