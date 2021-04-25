"""
This Django project created by Taylor Vance (Austin Pilgrimage #44)
A rewrite of Mike Dempsey's (Austin Presbyterian Cursillo #6) original prayerbanner.org

====

Django settings for prayerbanner project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

import environ
from pathlib import Path

# https://django-environ.readthedocs.io/en/latest/
env = environ.Env()
environ.Env.read_env()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool('DEBUG', False)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS', [])


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    'tz_detect',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'flatpickr',
    'tinymce',
    'captcha',

    'website.apps.WebsiteConfig',
    'banners.apps.BannersConfig',
    'accounts.apps.AccountsConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'tz_detect.middleware.TimezoneMiddleware',
    'accounts.middleware.UserTimezoneMiddleware',
]

ROOT_URLCONF = 'prayerbanner.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / 'templates',
            BASE_DIR / 'templates' / 'allauth',
        ],
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

WSGI_APPLICATION = 'prayerbanner.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases
# See "db_url" on https://django-environ.readthedocs.io/en/latest/#supported-types
DATABASES = {
    'default': env.db_url('DATABASE_URL', default='sqlite:////tmp/prayerbanner-db.sqlite3')
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]


# This expands into EMAIL_BACKEND, EMAIL_HOST, EMAIL_PORT, EMAIL_HOST_USER, and EMAIL_HOST_PASSWORD
# SMTP example: EMAIL_URL=smtp://user:password@prayerbanner.org:25
# See "email_url" on https://django-environ.readthedocs.io/en/latest/#supported-types
EMAIL_CONFIG = env.email_url('EMAIL_URL', default='consolemail://')
vars().update(EMAIL_CONFIG)

EMAIL_USE_TLS = False

DEFAULT_FROM_EMAIL = env.str('DEFAULT_FROM_EMAIL', default='admin@localhost')


# Overriding these tags (css classes) for Bootstrap
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.DEBUG: 'alert alert-secondary',
    messages.INFO: 'alert alert-info',
    messages.SUCCESS: 'alert alert-success',
    messages.WARNING: 'alert alert-warning',
    messages.ERROR: 'alert alert-danger',
}

# Settings for the WYSIWYG editor
# https://django-tinymce.readthedocs.io/en/latest/installation.html#configuration
# https://www.tiny.cloud/docs/general-configuration-guide/
TINYMCE_DEFAULT_CONFIG = {
    'force_br_newlines': True,
    'force_p_newlines': False,
    'forced_root_block': '',
    'plugins': 'code lists table',
    'menubar': False,
    'toolbar': 'undo redo | bold italic underline | fontsizeselect formatselect | numlist bullist table | code',
}


# Internationalization
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

USE_I18N = True

USE_L10N = True

USE_TZ = True
TIME_ZONE = 'UTC'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]


LOGIN_REDIRECT_URL = '/'

AUTH_USER_MODEL = 'accounts.User'


# This is required for allauth
SITE_ID = 1

# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_CONFIRM_EMAIL_ON_GET = True
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = env.str('ACCOUNT_EMAIL_VERIFICATION', 'mandatory')
ACCOUNT_FORMS = {
    'signup': 'accounts.forms.MySignupForm',
}
ACCOUNT_LOGIN_ON_EMAIL_CONFIRMATION = True
ACCOUNT_LOGIN_ON_PASSWORD_RESET = True
ACCOUNT_PRESERVE_USERNAME_CASING = False
ACCOUNT_USER_DISPLAY = lambda user: user.get_full_name()
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_USERNAME_REQUIRED = False

CAPTCHA_FONT_SIZE = 32
