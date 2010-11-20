import os

#for debug toolbar
INTERNAL_IPS = ('127.0.0.1',)


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

PROJECT_ROOT = os.path.realpath(os.path.dirname(__file__))

MANAGERS = ADMINS

TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'static')

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/media/'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = ('django.core.context_processors.media',
                               'django.core.context_processors.request',
                               'django.core.context_processors.auth',)
  

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

ROOT_URLCONF = 'sarahfoote.urls'

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates')
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'sarahfoote.main',
    'ckeditor',
    'django_extensions',    
)

LOGIN_URL = '/login'

CKEDITOR_MEDIA_PREFIX = "/static/ckeditor/"
CKEDITOR_UPLOAD_PATH = os.path.join(MEDIA_ROOT, 'photos')
CKEDITOR_SKIN = "kama"
CKEDITOR_TOOLBAR = """[
    ['Source','-'],
    ['Cut','Copy','Paste','PasteText','PasteFromWord','-','Print', 'SpellChecker', 'Scayt'],
    ['Undo','Redo','-','Find','Replace','-','SelectAll','RemoveFormat'],
    ['Bold','Italic','Underline','Strike','-','Subscript','Superscript'],
    ['NumberedList','BulletedList','-','Outdent','Indent','Blockquote','CreateDiv'],
    ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
    ['Link','Unlink','Anchor'],
    ['Image', 'Table','HorizontalRule', 'SpecialChar'],
    ['Styles','Format','Font','FontSize'],
    ['TextColor','BGColor'],
    ['Maximize', 'ShowBlocks']
]"""
CKEDITOR_HEIGHT = "291"
CKEDITOR_WIDTH = "618"
CKEDITOR_BROWSE_WIDTH = "800"
CKEDITOR_BROWSE_HEIGHT = "500"

# Add debug toolbar if you're debugging.
if DEBUG:
    LOCAL_MIDDLEWARE_CLASSES = (
        'debug_toolbar.middleware.DebugToolbarMiddleware',        
    )
    LOCAL_INSTALLED_APPS =(
        'debug_toolbar',
    )

try:
    from local_settings import *
except ImportError:
    pass
