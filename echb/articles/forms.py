from .models import Comment
from django.forms import modelformset_factory, TextInput, Textarea

NotAuthorizedCommentForm = modelformset_factory(Comment,
                                                fields=('name', 'email', 'body'),
                                                widgets={
                                                    'name': TextInput(
                                                        attrs={'placeholder': 'Ваше имя', 'class': 'form__text'}),
                                                    'email': TextInput(
                                                        attrs={'placeholder': 'Ваш Email', 'class': 'form__text'}),
                                                    'body': Textarea(
                                                        attrs={'placeholder': 'Вашe cообщение', 'class': 'form__text', 'rows': 5})
                                                },
                                                labels={
                                                    'name': '',
                                                    'email': '',
                                                    'body': ''
                                                })
AuthorizedCommentForm = modelformset_factory(Comment,
                                             fields=('body',),
                                             widgets={
                                                 'body': Textarea(
                                                     attrs={'placeholder': 'Вашe cообщение', 'class': 'form__text', 'rows': 5})
                                             },
                                             labels={
                                                 'body': ''
                                             })
