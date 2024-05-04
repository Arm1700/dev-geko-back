"""
Django settings for geko project.

Generated by 'django-admin startproject' using Django 5.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

from pathlib import Path
import os
from django.template.context_processors import static
import environ

# Load environment variables from .env file if present
environ.Env.read_env()

# Initialize environ
env = environ.Env()

# Загрузка переменных окружения из файла .env
PROJECT_DIR = os.path.dirname(__file__)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-vj_r0q!g7*vl6owfl6qhh^@4-9$91@j_a825qaopycceyrya2e'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
# DEBUG = False

SITE_ID = 1

ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'main',
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',
]

CORS_ALLOWED_ORIGINS = [
    'https://gekoeducation.com',
    'https://www.gekoeducation.com'
]

CSRF_TRUSTED_ORIGINS = [
    'https://gekoeducation.com',
    'https://www.gekoeducation.com'
]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'geko.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = '587'
EMAIL_USE_TLS = 'True'
EMAIL_HOST_USER = 'bukboks1@gmail.com'
EMAIL_HOST_PASSWORD = 'vayp irew pyny niui'
DEFAULT_FROM_EMAIL = 'bukboks1@gmail.com'

WSGI_APPLICATION = 'geko.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}
# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    }
}

# swagger
SPECTACULAR_SETTINGS = {
    'TITLE': 'Мое API',
    'DESCRIPTION': 'Описание моего API',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': True,
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

# STATIC_URL = "static/"

# Remove the nonexistent directory from STATICFILES_DIRS
# STATICFILES_DIRS = []
#
# STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Set STATIC_ROOT to a valid path
STATIC_URL = '/static/'

# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static'),
# ]

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
