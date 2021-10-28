from pathlib import Path
import os
import sys
from pathlib import Path
from typing import List
import environ

env: environ.Env = environ.Env()
environ.Env.read_env()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY: str = env('SECRET_KEY')


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = bool = env('DEBUG')

ALLOWED_HOSTS:  List[str] = env.list('ALLOWED_HOSTS')



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    #apps
    'api',
    # DRF stuff
    'rest_framework',
    'rest_framework.authtoken',
    'dj_rest_auth',
    'dj_rest_auth.registration',
    'rest_framework_swagger',
    # allauth
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.github',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'github_projects_tracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'libraries': {
                'staticfiles': 'django.templatetags.static',
            }
        },
    },
]

WSGI_APPLICATION = 'github_projects_tracker.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('POSTGRES_NAME'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('POSTGRES_HOST'),
        'PORT': env('POSTGRES_PORT'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =====CUSTOM ADDONS=====

# ALLAUTH
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend', # todo check
]

SITE_ID = 1

# DJANGO REST FRAMEWORK
REST_FRAMEWORK = { # TODO adjust
#     'DEFAULT_AUTHENTICATION_CLASSES': (
#         'rest_framework.authentication.SessionAuthentication',
#         'rest_framework.authentication.TokenAuthentication',
#     ),
#     'DEFAULT_PERMISSION_CLASSES': (
#             'rest_framework.permissions.IsAuthenticated',
#     ),
#     'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
#     'PAGE_SIZE': 25,
#     'DEFAULT_FILTER_BACKENDS': [
#         'django_filters.rest_framework.DjangoFilterBackend'
#     ],
#     'DEFAULT_THROTTLE_CLASSES': [
#         'rest_framework.throttling.AnonRateThrottle',
#         'rest_framework.throttling.UserRateThrottle'
#     ],
#     'DEFAULT_THROTTLE_RATES': {
#         'anon': '1000/day',
#         'user': '1000/day'
#     },
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
}

# DEBUG_TOOLBAR_CONFIG
DEBUG_TOOLBAR = env.bool('DEBUG_TOOLBAR', default=False)
if DEBUG and DEBUG_TOOLBAR:
    INTERNAL_IPS = [
        '127.0.0.1',
    ]
    DEBUG_TOOLBAR_CONFIG = {
        'SHOW_TOOLBAR_CALLBACK': lambda debug: DEBUG,
    }
    MIDDLEWARE.append('debug_toolbar.middleware.DebugToolbarMiddleware')
    INSTALLED_APPS.append('debug_toolbar')