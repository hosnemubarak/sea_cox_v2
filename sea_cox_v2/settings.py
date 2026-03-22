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

ALLOWED_HOSTS = ['*', 'www.seacoxsfire.com', 'seacoxsfire.com']

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

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.static',
                'django.template.context_processors.media',
                'home.context_processors.site_info',
            ],
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

# Security headers (for production)
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'SAMEORIGIN'


# =============================================================================
# LOGGING CONFIGURATION
# =============================================================================
# Log directory — auto-created on startup
LOG_DIR = BASE_DIR / 'logs'

# Ensure the log directory exists before Django configures handlers
from core.logging_utils import ensure_log_directory  # noqa: E402
ensure_log_directory()

# Maximum log file size and backup count
LOG_MAX_BYTES = int(os.environ.get('LOG_MAX_BYTES', 5 * 1024 * 1024))     # 5 MB
LOG_BACKUP_COUNT = int(os.environ.get('LOG_BACKUP_COUNT', 10))             # Keep 10 backups

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
            'maxBytes': 10 * 1024 * 1024,       # 10 MB (debug can be chatty)
            'backupCount': 5,
            'formatter': 'verbose',
            'encoding': 'utf-8',
            'filters': ['require_debug_true'],
        },

        # Mail admins on ERROR+ in production (requires EMAIL config)
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'formatter': 'verbose',
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
            'handlers': ['error_file', 'mail_admins'],
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
            'handlers': ['error_file', 'mail_admins'],
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
