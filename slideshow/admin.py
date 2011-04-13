from django.contrib import admin
from models import SlideShowImage

class SlideShowImageAdmin(admin.ModelAdmin):
    model = SlideShowImage

admin.site.register(SlideShowImage, SlideShowImageAdmin)
