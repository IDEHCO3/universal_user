"""
Django settings for universal_user project.

Generated by 'django-admin startproject' using Django 1.8.3.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import json
import datetime

with open("settings.json") as dt:
    settings_json = json.loads(dt.read())
FB = settings_json['facebook']

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

STATIC_ROOT = os.path.join(BASE_DIR, 'static_root/')

STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, "static"),
]

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'mwn6)v29l3r!@&4-8ohnx03v^h0-*x&2=qz!1w#@qj9d4=4sm9'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'rest_framework',
    'rest_framework_jwt',
    'users',
    'authentication',
    'create_user',
)

JWT_AUTH = {
    'JWT_VERIFY': True,
    'JWT_EXPIRATION_DELTA': datetime.timedelta(seconds=300),
    'JWT_ALLOW_REFRESH': True,
    'JWT_REFRESH_EXPIRATION_DELTA': datetime.timedelta(days=7),
    'JWT_PAYLOAD_HANDLER': 'authentication.utils.new_payload_handler',
}

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    ),
}

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    #OLD
    #'django.contrib.sessions.middleware.SessionMiddleware',
    #'django.middleware.common.CommonMiddleware',
    #'django.middleware.csrf.CsrfViewMiddleware',
    #'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    #'django.contrib.messages.middleware.MessageMiddleware',
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
    #'django.middleware.security.SecurityMiddleware',
)

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'universal_user.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'universal_user.wsgi.application'

if not 'IP_SGBD' in os.environ:
    os.environ['IP_SGBD'] = '172.17.0.2'

if not 'PORT_SGBD' in os.environ:
    os.environ['PORT_SGBD'] = '5432'

if not 'DATABASE_NAME' in os.environ:
    os.environ['DATABASE_NAME'] = 'idehco3'

if not 'USER_NAME_DATABASE' in os.environ:
    os.environ['USER_NAME_DATABASE'] = 'idehco3'

if not 'PASSWORD_DATABASE' in os.environ:
    os.environ['PASSWORD_DATABASE'] = 'idehco3'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
ip_sgbd = os.environ['IP_SGBD']
port_sgbd = os.environ['PORT_SGBD']
database_name = os.environ['DATABASE_NAME']
user_name_database = os.environ['USER_NAME_DATABASE']
password_database = os.environ['PASSWORD_DATABASE']

DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'HOST': ip_sgbd,
         'PORT': port_sgbd,
         'NAME': database_name,
         'USER': user_name_database,
         'PASSWORD': password_database
     }
}


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/universaluser/static/'

AUTH_USER_MODEL = 'users.User'



