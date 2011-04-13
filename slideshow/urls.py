from django.conf.urls.defaults import *
from slideshow.views import get_images

urlpatterns = patterns('',
    url('images', get_images, name='slideshow_get_images'),
)
