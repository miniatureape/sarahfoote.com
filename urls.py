from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.views import logout, login
from django.views.static import serve

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
    (r'^ckeditor/', include('ckeditor.urls')),    
    url(r'^logout/', logout,{'next_page': '/'}, name="logout"),
    url(r'^login/', login, {'template_name': 'login.html',}, name="login"),
    (r'^', include('sarahfoote.main.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^static/(?P<path>.*)', serve, {'document_root': settings.MEDIA_ROOT}),                           
    )
