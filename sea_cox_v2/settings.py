"""
Django settings for sea_cox_v2 — fully static, no database.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-seacoxv2-static-site-key-change-in-production')

DEBUG = os.environ.get('DEBUG', 'False').lower() in ['true', '1', 't']

ALLOWED_HOSTS = os.environ.get(
    'ALLOWED_HOSTS',
    'localhost,127.0.0.1,seacoxsfire.com,www.seacoxsfire.com'
).split(',')

INSTALLED_APPS = [
    'django.contrib.staticfiles',
    'home',
    'core',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'core.middleware.RequestResponseLoggingMiddleware',
]

ROOT_URLCONF = 'sea_cox_v2.urls'

# Template loaders — cache compiled templates in production
_TEMPLATE_LOADERS = [
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
]
if not DEBUG:
    _TEMPLATE_LOADERS = [
        ('django.template.loaders.cached.Loader', _TEMPLATE_LOADERS),
    ]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.media',
                'home.context_processors.site_info',
            ],
            'loaders': _TEMPLATE_LOADERS,
        },
    },
]

WSGI_APPLICATION = 'sea_cox_v2.wsgi.application'

# No database
DATABASES = {}

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Dubai'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
    },
}

# Tell Whitenoise to not complain if it can't find files like .map sourcemaps referenced in CSS/JS
WHITENOISE_MANIFEST_STRICT = False

# Media files (previously uploaded images)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Security headers
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'

# Production-only security hardening
if not DEBUG:
    SECURE_SSL_REDIRECT = os.environ.get('SECURE_SSL_REDIRECT', 'True').lower() in ['true', '1', 't']
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True


# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================
from core.logging_utils import get_safe_log_directory

# Get a safe, writable log directory (falls back to /tmp/logs if needed)
LOG_DIR = get_safe_log_directory(BASE_DIR)

# Maximum log file size and backup count (conservative for shared hosting)
LOG_MAX_BYTES = int(os.environ.get('LOG_MAX_BYTES', 2 * 1024 * 1024))     # 2 MB
LOG_BACKUP_COUNT = int(os.environ.get('LOG_BACKUP_COUNT', 3))              # Keep 3 backups

# Shared log format
LOG_FORMAT = (
    "[{asctime}] {levelname} | {name} | {filename}:{lineno} | {message}"
)
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    # ── Formatters ─────────────────────────────────────────────────
    'formatters': {
        'verbose': {
            'format': LOG_FORMAT,
            'style': '{',
            'datefmt': LOG_DATE_FORMAT,
        },
        'simple': {
            'format': '[{asctime}] {levelname} | {message}',
            'style': '{',
            'datefmt': LOG_DATE_FORMAT,
        },
    },

    # ── Filters ────────────────────────────────────────────────────
    'filters': {
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },

    # ── Handlers ───────────────────────────────────────────────────
    'handlers': {
        # Console output (always active, level controlled per logger)
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },

        # ERROR log file — captures ERROR and CRITICAL only
        'error_file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR / 'error.log'),
            'maxBytes': LOG_MAX_BYTES,
            'backupCount': LOG_BACKUP_COUNT,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },

        # INFO log file — captures INFO, WARNING, ERROR, CRITICAL
        'info_file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR / 'info.log'),
            'maxBytes': LOG_MAX_BYTES,
            'backupCount': LOG_BACKUP_COUNT,
            'formatter': 'verbose',
            'encoding': 'utf-8',
        },

        # DEBUG log file — ONLY active in development (DEBUG=True)
        'debug_file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR / 'debug.log'),
            'maxBytes': 5 * 1024 * 1024,        # 5 MB
            'backupCount': 2,
            'formatter': 'verbose',
            'encoding': 'utf-8',
            'filters': ['require_debug_true'],
        },
    },

    # ── Loggers ────────────────────────────────────────────────────
    'loggers': {
        # Root Django logger
        'django': {
            'handlers': ['console', 'info_file', 'error_file'],
            'level': 'INFO',
            'propagate': True,
        },

        # Django request/response errors (4xx, 5xx)
        'django.request': {
            'handlers': ['error_file'],
            'level': 'ERROR',
            'propagate': False,
        },

        # Django server (runserver output)
        'django.server': {
            'handlers': ['console', 'info_file'],
            'level': 'INFO',
            'propagate': False,
        },

        # Django template rendering errors
        'django.template': {
            'handlers': ['error_file', 'console'],
            'level': 'ERROR',
            'propagate': False,
        },

        # Django security issues
        'django.security': {
            'handlers': ['error_file'],
            'level': 'WARNING',
            'propagate': False,
        },

        # ── Application loggers ────────────────────────────────────
        # Main project-level logger (sea_cox_v2.*)
        'sea_cox_v2': {
            'handlers': ['console', 'info_file', 'error_file', 'debug_file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },

        # Request/response middleware logger
        'sea_cox_v2.request': {
            'handlers': ['console', 'info_file', 'error_file'],
            'level': 'INFO',
            'propagate': False,
        },

        # Home app logger
        'home': {
            'handlers': ['console', 'info_file', 'error_file', 'debug_file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },

        # Core utilities logger
        'core': {
            'handlers': ['console', 'info_file', 'error_file', 'debug_file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}
