import os
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

# ============================================================================
# BASE DIRECTORY
# ============================================================================
BASE_DIR = Path(__file__).resolve().parent.parent

# ============================================================================
# ENVIRONMENT VARIABLES HELPER
# ============================================================================
def get_env_variable(var_name, default=None, required=True):
    """
    Get environment variable or raise exception if required.

    Args:
        var_name: Name of the environment variable
        default: Default value if not required
        required: If True, raises error when variable is missing

    Returns:
        The value of the environment variable
    """
    value = os.environ.get(var_name, default)
    if required and value is None:
        raise ImproperlyConfigured(
            f"Missing required environment variable: {var_name}\n"
            f"Please add it to your .env file or set it in the environment."
        )
    return value

# ============================================================================
# SECURITY SETTINGS
# ============================================================================
SECRET_KEY = get_env_variable('SECRET_KEY')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Only allow specific hosts - no wildcards in production!
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# CSRF trusted origins (for production)
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')

# ============================================================================
# APPLICATION DEFINITION
# ============================================================================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'alumni',
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

ROOT_URLCONF = 'alumni_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'alumni_project.context_processors.brand_colors',
            ],
        },
    },
]

WSGI_APPLICATION = 'alumni_project.wsgi.application'

# ============================================================================
# DATABASE SETTINGS
# ============================================================================
# Use DATABASE_URL if provided, otherwise fallback to SQLite
if os.environ.get('DATABASE_URL'):
    # Convert postgres:// to postgresql:// for compatibility
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            ssl_require=True  # Required for PythonAnywhere MySQL/PostgreSQL
        )
    }
else:
    # Fallback to SQLite for local development
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# ============================================================================
# PASSWORD VALIDATION
# ============================================================================
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 8,
        }
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# ============================================================================
# INTERNATIONALIZATION
# ============================================================================
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Asia/Kolkata'  # Indian Time
USE_I18N = True
USE_TZ = True

# ============================================================================
# STATIC & MEDIA FILES
# ============================================================================
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# File storage for PythonAnywhere (use default)
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

# ============================================================================
# DEFAULT AUTO FIELD
# ============================================================================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# ============================================================================
# CUSTOM USER MODEL
# ============================================================================
AUTH_USER_MODEL = 'alumni.User'

# ============================================================================
# CUSTOM SITE SETTINGS
# ============================================================================
# Brand colors
SITE_PRIMARY_COLOR = os.environ.get('SITE_PRIMARY_COLOR', '#901d78')
SITE_SECONDARY_COLOR = os.environ.get('SITE_SECONDARY_COLOR', '#7a1866')
SITE_NAME = os.environ.get('SITE_NAME', 'AlumniConnect')

# Departments
DEPARTMENTS = [
    ('CSE', 'Computer Science and Engineering'),
    ('ECE', 'Electronics and Communication Engineering'),
    ('MECH', 'Mechanical Engineering'),
    ('CE', 'Civil Engineering'),
    ('EEE', 'Electrical and Electronics Engineering'),
    ('IT', 'Information Technology'),
    ('AIME', 'Automobile and Industrial Engineering'),
    ('BTECH', 'Biotechnology'),
    ('MBA', 'MBA'),
    ('MCA', 'MCA'),
    ('MTECH', 'M.Tech'),
    ('MSc', 'M.Sc'),
    ('PhD', 'PhD'),
    ('OTHER', 'Others'),
]

# ============================================================================
# EMAIL SETTINGS
# ============================================================================
# All email settings are now pulled from environment variables!
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = get_env_variable('EMAIL_HOST', 'smtp.gmail.com', required=False)
EMAIL_PORT = int(os.environ.get('EMAIL_PORT', 587))
EMAIL_HOST_USER = get_env_variable('EMAIL_HOST_USER', 'info@alumniconnect.org', required=False)
EMAIL_HOST_PASSWORD = get_env_variable('EMAIL_HOST_PASSWORD')  # REQUIRED - from .env
EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', 'True') == 'True'
EMAIL_USE_SSL = os.environ.get('EMAIL_USE_SSL', 'False') == 'True'
DEFAULT_FROM_EMAIL = os.environ.get('DEFAULT_FROM_EMAIL', f'AlumniConnect <{EMAIL_HOST_USER}>')

# ============================================================================
# LOGGING (Optional but recommended for debugging)
# ============================================================================
if DEBUG:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
            },
        },
        'root': {
            'handlers': ['console'],
            'level': 'WARNING',
        },
        'loggers': {
            'django': {
                'handlers': ['console'],
                'level': os.environ.get('DJANGO_LOG_LEVEL', 'INFO'),
                'propagate': False,
            },
        },
    }

# ============================================================================
# SECURITY SETTINGS FOR PRODUCTION
# ============================================================================
if not DEBUG:
    # HTTPS settings (for PythonAnywhere production)
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

    # Security headers
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'