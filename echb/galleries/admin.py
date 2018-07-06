from django.contrib import admin
from django.urls import path
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.contrib.admin import helpers

from .models import *
from .forms import UploadZipForm

admin.site.register(Tag)
admin.site.register(Author)

class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'gallery', 'image_thumb')
    list_filter = ['gallery']
    list_per_page = 20
    readonly_fields = ["image_thumb"]

admin.site.register(Image, ImageAdmin)

class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title','date','slug','main_image','author')
    list_filter = ['date','author','tags']
    search_fields = ['title', 'slug']
    readonly_fields = ['image_count']
    list_per_page = 20

    def get_urls(self):
        urls = super(GalleryAdmin, self).get_urls()
        custom_urls = [
            path('upload_zip/', self.admin_site.admin_view(self.upload_zip), name='upload_zip')
        ]
        return custom_urls + urls

    def upload_zip(self, request):
        context = {
            'title': "Загрузить .zip файл с фотографиями",
            'app_label': self.model._meta.app_label,
            'opts': self.model._meta,
            'has_change_permission': self.has_change_permission(request)
        }

        # Handle form request
        if request.method == 'POST':
            form = UploadZipForm(request.POST, request.FILES)
            if form.is_valid():
                form.save(request=request)
                return HttpResponseRedirect('..')
        else:
            form = UploadZipForm()
        context['form'] = form
        context['adminform'] = helpers.AdminForm(form,
                                                 list([(None, {'fields': form.base_fields})]),
                                                 {})
        return render(request, 'admin/galleries/upload_zip.html', context)

admin.site.register(Gallery, GalleryAdmin)