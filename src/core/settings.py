"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 2.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'r(o1lsq=vk=x)e7n-&&3b21)e^gmfhbcgh+ad#@1gct+=!%@_a'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

AUTH_USER_MODEL = 'accounts.User'

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # postgres
    'django.contrib.postgres',
    # for array plus button but admin site
    'django_better_admin_arrayfield.apps.DjangoBetterAdminArrayfieldConfig',

    # for datetime picker
    "bootstrap4",
    "bootstrap_datepicker_plus",

    # third party
    'crispy_forms',
    'markdown_deux',
    'pagedown',
    'notifications',

    # local apps
    'accounts',
    'article',
    'comments',
    'cq',
    'cqexam',
    'exam',
    'level',
    'mcq',
    'mcqexam',
    # 'posts',
    'course',
    'student',
    'teacher',
    'room',
]

# added by belal from trdjango19
CRISPY_TEMPLATE_PACK = 'bootstrap4'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# added by belal from trdjango19
LOGIN_URL = "/login/"

ROOT_URLCONF = 'core.urls'

DJANGO_NOTIFICATIONS_CONFIG = {'USE_JSONFIELD': True}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),
                 os.path.join(BASE_DIR, 'templates/accounts'),
                 os.path.join(BASE_DIR, 'templates/article'),
                 os.path.join(BASE_DIR, 'templates/comments'),
                 os.path.join(BASE_DIR, 'templates/cq'),
                 os.path.join(BASE_DIR, 'templates/cqexam'),
                 os.path.join(BASE_DIR, 'templates/exam'),
                 os.path.join(BASE_DIR, 'templates/mcq'),
                 os.path.join(BASE_DIR, 'templates/mcqexam'),
                 os.path.join(BASE_DIR, 'templates/posts'),
                 os.path.join(BASE_DIR, 'templates/room'),
                 os.path.join(BASE_DIR, 'templates/teacher'),
                 os.path.join(BASE_DIR, 'templates/student'),
                 os.path.join(BASE_DIR, 'VisualMathEditor'),
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

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'openeduqa-v0-0',
        'USER': 'dbuser',
        'PASSWORD': 'dbpassword',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_URL = '/static/'


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static"),
    # '/var/www/static/',
]

STATIC_ROOT = os.path.join(os.path.dirname(BASE_DIR), "static_cdn")

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(os.path.dirname(BASE_DIR), "media_cdn")
