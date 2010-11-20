from django.conf.urls.defaults import *
from django.views.generic.create_update import update_object
from django.views.generic.create_update import create_object
from django.views.generic.create_update import delete_object
from django.views.generic.list_detail import object_list
from django.views.generic.list_detail import object_detail
from django.views.generic.date_based import archive_year
from django.views.generic.date_based import archive_index
from django.views.generic.date_based import archive_month

from main.views import home, add_photo, publish_post, buy_category, contact, about, items, items_by_category, handle_pop_up, add_file
from main.models import BlogPost, Item, Photo, About, Press, File
from main.models import select, select_latest, select_attr, get_about
from main.forms import BlogPostForm, PhotoForm, ItemForm, PressForm

urlpatterns = patterns('',
    
    # Press
    url(r'^press/add', create_object, {
        'model': Press,
        'login_required': True,
        'template_name': 'add-form.html',
        'form_class': PressForm,
        'post_save_redirect' : '/press',
        'extra_context': {'cancel': '/press'},        
        }, name="main_add_press"        
    ),
    url(r'^press/delete/(?P<object_id>[0-9]+)', delete_object, {
        'model': Press,
        'login_required': True,
        'template_name': 'confirm-delete.html',
        'post_delete_redirect' : '/press',
        'template_name': 'confirm-delete.html',
        }, name="main_delete_press"
    ),
    url(r'^press/edit/(?P<object_id>[0-9]+)', update_object, {
        'model': Press,
        'login_required': True,
        'form_class': PressForm,
        'template_name': 'edit-form.html',
        'post_save_redirect' : '/press',
        }, name="main_edit_press"
    ),
    url(r'^press', object_list, {
        'queryset': select(Press),
        'template_object_name': 'press',
        'template_name': 'press.html',
        }, name="main_list_press"
    ),
    # About
    url(r'^about/edit/(?P<object_id>[0-9]+)', update_object, {
        'model': About,
        'login_required': True,
        'template_name': 'edit-form.html',
        'post_save_redirect': '/about',
        }, name="main_edit_about"
    ),
    url(r'^about/add', create_object, {
        'model': About,
        'login_required': True,
        'template_name': 'add-form.html',
        'post_save_redirect': '/about',
        }, name="main_add_about"),
    url(r'^about', about, name="main_about"),    

    # Photo
    url(r'^photos/add', add_photo, name="main_add_photos"),

    # File
    url(r'^file/add', add_file, name="main_add_file"),
   
    
    # Items
    url(r'^items/category/(?P<category>.*)', items_by_category, name="main_list_items_by_category"),
    url(r'^items/edit/(?P<object_id>[0-9]+)', update_object, {
        'model': Item,
        'login_required': True,
        'form_class': ItemForm,        
        'template_name': 'edit-form.html',
        'post_save_redirect' : '/items',
        }, name="main_edit_item"        
    ),
    
    url(r'^items/add', create_object, {
        'model': Item,
        'login_required': True,
        'form_class': ItemForm,
        'template_name': 'add-form.html',
        'post_save_redirect' : '/items',
        'extra_context': {'cancel': '/items'},        
        }, name="main_add_item"        
    ),
    url(r'^items/(?P<slug>.+)', object_detail, {
        'template_name': 'item-detail.html',
        'queryset': select(Item),
        'slug_field': 'slug',
        'template_object_name': 'item',
        'extra_context': {'categories': select_attr(Item, 'category')}
        },
        name="main_item_detail"),    
    url(r'^items', items, name="main_list_items"),

    # Blog Posts
    url(r'^post/add', create_object, {
        'form_class': BlogPostForm,
        'login_required': True,
        'template_name': 'add-form.html',
        'post_save_redirect' : '/posts',
        'extra_context': {'cancel': '/posts'},
        }, name="main_add_post"        
    ),
    url(r'^post/edit/(?P<object_id>[0-9]+)', update_object, {
        'form_class': BlogPostForm,
        'login_required': True,
        'template_name': 'edit-form.html',
        'post_save_redirect' : '/posts',
        }, name="main_edit_post"        
    ),
    url(r'^posts/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})', archive_month, {
        'template_name': 'blogpost_archive_month.html',
        'date_field': 'published_on',
        'month_format': '%m',
        'queryset': select(BlogPost),
        'allow_empty': True,
        'template_object_name': 'posts'
        }
        ,name="main_posts_month"),    
    url(r'^posts/(?P<year>[0-9]{4})', archive_year, {
        'template_name': 'blogpost_archive_year.html',
        'date_field': 'published_on',
        'make_object_list': True,
        'queryset': select(BlogPost),
        'template_object_name': 'posts'
        }        
        ,name="main_posts_year"),    
    url(r'^posts', archive_index, {
        'template_name': 'blog-index.html',
        'queryset': select(BlogPost),
        'date_field': 'published_on',
        'num_latest': 5,
        'template_object_name': 'posts_list'
        }
        ,name="main_post_list"),    
    url(r'^post/publish/(?P<object_id>[0-9]+)', publish_post, name="main_publish_post"),
    url(r'^post/(?P<slug>.+)', object_detail,
        {'template_name': 'blog-detail.html',
         'queryset': select(BlogPost),
         'slug_field': 'slug',
         'template_object_name': 'post'},
        name="main_post_detail"),
    
    # Contact
    url(r'^contact', contact, name="main_contact"),
    
    # Home
    url(r'^$', items, name="main_home"),
    #url(r'^$', home, name="main_home"),
)
