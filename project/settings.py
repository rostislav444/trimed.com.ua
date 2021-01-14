import os
from django.utils.translation import ugettext_lazy as _
from .local_settings import *


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, 'templates')
STATICFILE_DIR  = os.path.join(BASE_DIR, 'static')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vitk-%hv%#r#c*_@wq6)8*ybx!33=!(i6w8-dna2u+-f)ubc_g'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

APPEND_SLASH = True

ALLOWED_HOSTS = [
    'ukrchitrade.top','www.ukrchitrade.top',
    '185.233.119.159','127.0.0.1',
    'localhost'
]

# Application definition

INSTALLED_APPS = [
    # dajngo modules
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # apps
    'apps.blog.apps.BlogConfig',
    'apps.cart',
    'apps.catalogue.apps.CatalogueConfig',
    'apps.core',
    'apps.comments.apps.CommentsConfig',
    'apps.currency.apps.CurrencyConfig',
    'apps.catalogue_filters.apps.CatalogueFiltersConfig',
    'apps.documents.apps.DocumentsConfig',
    'apps.user.apps.UserConfig',
    'apps.order.apps.OrderConfig',
    'apps.search',
    'apps.shop.apps.ShopConfig',
    'apps.pages.apps.PagesConfig',
    # libs
    'ckeditor',
    'rest_framework',
    "compressor",
    'autotranslate',
    'mptt',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
]

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATE_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'apps.core.context_processors.language_change',
                'apps.core.context_processors.main_data',
                'apps.cart.context_processors.cart',
                'apps.catalogue.context_processors.categories',
                'apps.user.context_processors.wishlist',
                'apps.shop.context_processors.compare',
                'apps.pages.context_processors.static_pages',
            ],
            'builtins': [
                'apps.core.templatetags.tags',
            ]
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'





# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'ru'
TIME_ZONE = 'Europe/Kiev'
USE_TZ = True
USE_I18N = True
USE_L10N = True
USE_TZ = True

LANGUAGES = (
    # ('zh-hans', ('中国')),
    ('en', ('ENG')),
    ('ru', ('РУС')),
    ('uk', ('УКР')),
)


LOCALE_PATHS = [
    os.path.join(BASE_DIR, 'locale'),
]

CART_SESSION_ID = "cart"
WATCHLIST_SESSION_ID = "watchlist"
COMPARE_SESSION_ID = "compare"

AUTH_EXEMPT_ROUTES = ('admin:login')
AUTH_LOGIN_ROUTE = 'user:login'
LOGOUT_REDIRECT_URL = '/login/'
LOGIN_REDIRECT_URL = '/login/'
LOGIN_URL = ('user:authentication') 

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static_root/')
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_OFFLINE = True
COMPRESS_ENABLED = False
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')
STATICFILES_DIRS = [
    STATICFILE_DIR,
]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',

)

# User
AUTH_USER_MODEL = 'user.CustomUser'
ACCOUNT_AUTHENTICATION_METHOD = "email"
LOGOUT_REDIRECT_URL = '/'

AUTHENTICATION_BACKENDS = [
    'apps.user.auth.UserAuthentication',
]


CKEDITOR_UPLOAD_PATH = "media/uploads/"
CKEDITOR_CONFIGS = {
    'default': {
        'skin': 'office2013',
        # 'skin': 'office2013',
        'toolbar_Basic': [
            ['Source', '-', 'Bold', 'Italic']
        ],
        'toolbar_YourCustomToolbarConfig': [
            {'name': 'document', 'items': ['Source', '-', 'Save', 'NewPage', 'Preview', 'Print', '-', 'Templates']},
            {'name': 'clipboard', 'items': ['Cut', 'Copy', 'Paste', 'PasteText', 'PasteFromWord', '-', 'Undo', 'Redo']},
            {'name': 'editing', 'items': ['Find', 'Replace', '-', 'SelectAll']},
            {'name': 'forms',
             'items': ['Form', 'Checkbox', 'Radio', 'TextField', 'Textarea', 'Select', 'Button', 'ImageButton',
                       'HiddenField']},
            '/',
            {'name': 'basicstyles',
             'items': ['Bold', 'Italic', 'Underline', 'Strike', 'Subscript', 'Superscript', '-', 'RemoveFormat']},
            {'name': 'paragraph',
             'items': ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Blockquote', 'CreateDiv', '-',
                       'JustifyLeft', 'JustifyCenter', 'JustifyRight', 'JustifyBlock', '-', 'BidiLtr', 'BidiRtl',
                       'Language']},
            {'name': 'links', 'items': ['Link', 'Unlink', 'Anchor']},
            {'name': 'insert',
             'items': ['Image', 'Flash', 'Table', 'HorizontalRule', 'Smiley', 'SpecialChar', 'PageBreak', 'Iframe']},
            '/',
            {'name': 'styles', 'items': ['Styles', 'Format', 'FontSize']},
            {'name': 'colors', 'items': ['TextColor', 'BGColor']},
            {'name': 'tools', 'items': ['Maximize', 'ShowBlocks']},
            {'name': 'about', 'items': ['About']},
            '/',  # put this to force next toolbar on new line
            {'name': 'yourcustomtools', 'items': [
                # put the name of your editor.ui.addButton here
                'Preview',
                'Maximize',

            ]},
        ],
        'toolbar': 'YourCustomToolbarConfig',  # put selected toolbar config here
        # 'toolbarGroups': [{ 'name': 'document', 'groups': [ 'mode', 'document', 'doctools' ] }],
        # 'height': 291,
        # 'width': '100%',
        # 'filebrowserWindowHeight': 725,
        # 'filebrowserWindowWidth': 940,
        # 'toolbarCanCollapse': True,
        # 'mathJaxLib': '//cdn.mathjax.org/mathjax/2.2-latest/MathJax.js?config=TeX-AMS_HTML',
        'tabSpaces': 4,
        'extraPlugins': ','.join([
            'uploadimage', # the upload image feature
            # your extra plugins here
            'div',
            'autolink',
            'autoembed',
            'embedsemantic',
            # 'autogrow',
            # 'devtools',
            'widget',
            'lineutils',
            'clipboard',
            'dialog',
            'dialogui',
            'elementspath'
        ]),
    }
}

GMAIL_ADRESS = 'rostislav444@gmail.com'
GMAIL_PASSWORD = 'rideordie24'


EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = GMAIL_ADRESS
EMAIL_HOST_PASSWORD = GMAIL_PASSWORD
EMAIL_PORT = 587
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER


TELEGRAM_BOT = '1484777515:AAE_30QEs0Jb7_3mymgK0TYdTY2oD_M4orc'
TELEGRAM_CHANEL = '1289759082'
TELEGRAM_GET_LINK = 'https://api.telegram.org/bot'+ TELEGRAM_BOT  +'/sendMessage?chat_id=-100'+ TELEGRAM_CHANEL +'&text='
