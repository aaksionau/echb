"""A form to upload zipped file with photos

Raises:
    forms.ValidationError -- BadZipFile - the error raised for bad ZIP files
    forms.ValidationError -- some data in a Zip file (.zip or .zipx) is damaged.
    forms.ValidationError -- if gallery with user typed name already exists 
    forms.ValidationError -- if user typed gallery name and chose gallery from the list

Returns:
    on save return gallery id
"""

import logging
import os
import zipfile

from django import forms
from django.conf import settings
from django.contrib import messages
from django.core.files.base import ContentFile
from PIL import Image as PILImage
from unidecode import unidecode

from .models import Author, Gallery, Image, Tag

logger = logging.getLogger('ECHB')


class UploadZipForm(forms.Form):
    zip_file = forms.FileField()
    title = forms.CharField(max_length=150,
                            required=False,
                            help_text="Введите название галереи, если хотите создать новую")
    gallery = forms.ModelChoiceField(Gallery.objects.all(
    ), required=False, help_text='Выберите галерею для загрузки фотографий или оставьте пустой для создания новой')
    date = forms.DateField(help_text='Введите дату съемки фотографий')
    author = forms.ModelChoiceField(Author.objects.all(
    ), required=False, help_text="Выберите автора фотографий")
    tags = forms.ModelMultipleChoiceField(Tag.objects.all(), required=False)
    description = forms.CharField(required=False)

    def clean_zip_file(self):
        zip_file = self.cleaned_data['zip_file']
        try:
            zip = zipfile.ZipFile(zip_file)
        except zipfile.BadZipfile as ex:
            raise forms.ValidationError(str(ex))

        if zip.testzip():
            zip.close()

            raise forms.ValidationError('Файл содержит ошибки')

        zip.close()

        return zip_file

    def clean_title(self):
        title = self.cleaned_data['title']
        if title and Gallery.objects.filter(title=title).exists():
            raise forms.ValidationError(
                'Галерея с таким названием уже существует')

        return title

    def clean(self):
        cleaned_data = super(UploadZipForm, self).clean()

        if not self['title'].errors:
            if not cleaned_data.get('title', None) and not cleaned_data['gallery']:
                raise forms.ValidationError(
                    'Выберите галерею или введите название для галереи')
        return cleaned_data

    def resize_image(self, image_name, folder):

        base_path = os.path.join(settings.MEDIA_ROOT, 'galleries', folder)
        image_path = os.path.join(base_path, image_name)
        resized_image_path = os.path.join(base_path, 'small', image_name)

        basewidth = 300

        img = PILImage.open(image_path)
        wpercent = (basewidth / float(img.size[0]))
        hsize = int((float(img.size[1]) * float(wpercent)))
        img = img.resize((basewidth, hsize), PILImage.ANTIALIAS)
        if not os.path.exists(os.path.dirname(resized_image_path)):
            os.makedirs(os.path.dirname(resized_image_path))
        img.save(resized_image_path, quality=90)
        return resized_image_path

    def change_slug(self, slug):
        return unidecode(self.cleaned_data['title'].replace(' ', '-').lower())

    def save(self, request=None, zip_file=None):
        if not zip_file:
            zip_file = self.cleaned_data['zip_file']

        zip = zipfile.ZipFile(zip_file)

        if self.cleaned_data['gallery']:
            gallery = self.cleaned_data['gallery']
        else:
            author_id = self.cleaned_data['author']

        gallery = Gallery()
        gallery.title = self.cleaned_data['title']
        gallery.slug = self.change_slug(self.cleaned_data['title'])
        gallery.description = self.cleaned_data['description']
        gallery.date = self.cleaned_data['date']
        gallery.author = author_id

        gallery.save()

        first_image_index = 0
        first_image = ''
        for filename in sorted(zip.namelist()):

            if os.path.dirname(filename):
                continue

            if first_image_index == 0:
                first_image = f'{gallery.slug}/small/{filename}'
            first_image_index = +1
            data = zip.read(filename)
            image = Image(title=self.cleaned_data['title'], image=filename)
            image.gallery = gallery
            image.thumbnail = f'{gallery.slug}/small/{filename}'
            contentfile = ContentFile(data)
            image.image.save(filename, contentfile)

            self.resize_image(filename, gallery.slug)

        gallery.main_image.name = first_image
        gallery.save()

        zip.close()
        if request:
            messages.success(request,
                             'The photos have been added to gallery "{0}".'.format(
                                 gallery.title),
                             fail_silently=True)

            return gallery.pk
