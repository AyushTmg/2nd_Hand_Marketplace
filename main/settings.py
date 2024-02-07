import os 
from pathlib import Path



BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-=uf3%)4vs%nga#@l!$#x050xeyon4ghq)4+%1wlu&4b_x)&6rj'

DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = [
    "daphne",
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authentication',
    'marketplace',
    'chats',
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

ROOT_URLCONF = 'main.urls'

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
        },
    },
]

# ! Configurations for wsgi 
ASGI_APPLICATION = 'main.asgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME':os.environ.get("DB_NAME"),
        'USER': 'postgres', 
        'PASSWORD':os.environ.get("DB_PASS"), 
        'HOST': 'localhost', 

    }
}



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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LOGIN_URL = '/login/'
SIGN_UP_FIELDS=['first_name','last_name','username','email']
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# !Configurations For Static and Media Files 
STATIC_URL = 'static/'
STATIC_ROOT=os.path.join(BASE_DIR,'static')

MEDIA_URL='media/'
MEDIA_ROOT=os.path.join(BASE_DIR,'media')



# ! Configurations for Custom User Model 
AUTH_USER_MODEL='authentication.User'


# !Configurations for channel layers
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [("127.0.0.1", 6379)],
        },
    },
}

#! Configurations For Email
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER =os.environ.get('EMAIL')
EMAIL_HOST_PASSWORD = os.environ.get('EMAIL_PASSWORD')
DEFAULT_FROM_EMAIL = os.environ.get('EMAIL')



# !Configurations for Celery
CELERY_BROKER_URL = 'redis://localhost:6379/1'