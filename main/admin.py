from django.contrib import admin
from main.models import *
from django import forms

class PhotoAdmin(admin.ModelAdmin):
    pass

class BlogPostForm(admin.ModelAdmin):
    pass

class AboutAdmin(admin.ModelAdmin):
    pass

class PressAdmin(admin.ModelAdmin):
    pass

class FileAdmin(admin.ModelAdmin):
    pass

class ItemAdmin(admin.ModelAdmin):
    pass


admin.site.register(BlogPost, BlogPostForm)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(About, AboutAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(Press, PressAdmin)
admin.site.register(Item, ItemAdmin)
