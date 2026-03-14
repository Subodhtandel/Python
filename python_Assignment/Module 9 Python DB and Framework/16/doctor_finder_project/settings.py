"""
Django settings for doctor_finder_project project.
"""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-doctor-finder-paytm-key-change-in-production'

DEBUG = True

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'doctors',
    'payments',
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

ROOT_URLCONF = 'doctor_finder_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'doctor_finder_project.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Paytm Configuration
# IMPORTANT: Replace these with your actual Paytm credentials
# Get credentials from: https://business.paytm.com/

# For Testing/Staging (Use Paytm Test Credentials)
PAYTM_MERCHANT_ID = 'YOUR_MERCHANT_ID'
PAYTM_MERCHANT_KEY = 'YOUR_MERCHANT_KEY'
PAYTM_WEBSITE = 'WEBSTAGING'  # Use 'WEBSTAGING' for testing, 'DEFAULT' for production
PAYTM_CHANNEL_ID = 'WEB'
PAYTM_INDUSTRY_TYPE_ID = 'Retail'

# Paytm URLs
# Staging URLs
PAYTM_PAYMENT_GATEWAY_URL = 'https://securegw-stage.paytm.in/order/process'
PAYTM_TRANSACTION_STATUS_URL = 'https://securegw-stage.paytm.in/order/status'

# Production URLs (uncomment when going live)
# PAYTM_PAYMENT_GATEWAY_URL = 'https://securegw.paytm.in/order/process'
# PAYTM_TRANSACTION_STATUS_URL = 'https://securegw.paytm.in/order/status'

# Callback URL (update this with your actual domain)
PAYTM_CALLBACK_URL = 'http://127.0.0.1:8000/payments/paytm-callback/'


