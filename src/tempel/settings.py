DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
)

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'tempel.db'
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

TIME_ZONE = 'Asia/Jakarta'

LANGUAGE_CODE = 'en'

SITE_ID = 1

USE_I18N = False

import os
MEDIA_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media')
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/media/'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'dbb4413767843d993a472619e74bc9e3657815c21694f043f80d9a0857e428b5'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.core.context_processors.auth",
    "django.core.context_processors.i18n",
    "django.core.context_processors.request",
    "django.core.context_processors.media",
)

ROOT_URLCONF = 'tempel.urls'

TEMPLATE_DIRS = (
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'tempel',
)

def t(name, label, ext='txt', mime='text/plain'):
    return {'name': name, 'label': label, 'mime': mime, 'ext': ext}

TEMPEL_LANGUAGES = [
    t('bash',        'Bash',             'sh',       'text/x-sh'),
    t('c',           'C',                'c',        'text/x-csrc'),
    t('cpp',         'C++',              'cpp',      'text/x-c++src'),
    t('css',         'CSS',              'css',      'text/css'),
    t('diff',        'Diff',             'diff',     'text/x-diff'),
    t('html',        'HTML',             'html',     'text/html'),
    t('html+django', 'HTML+Django',      'html',     'text/html'),
    t('ini',         'INI',              'ini',      'text/plain'),
    t('java',        'Java',             'java',     'text/x-java'),
    t('lua',         'Lua',              'lua',      'text/plain'),
    t('make',        'Makefile',         'makefile', 'text/plain'),
    t('perl',        'Perl',             'pl',       'text/x-perl'),
    t('php',         'PHP',              'php',      'application/x-httpd-php'),
    t('python',      'Python',           'py',       'text/x-python'),
    t('rst',         'reStructuredText', 'rst',      'text/plain'),
    t('ruby',        'Ruby',             'rb',       'application/x-ruby'),
    t('sql',         'SQL',              'sql',      'text/plain'),
    t('text',        'Plain text',       'txt',      'text/plain'),
    t('xml',         'XML',              'xml',      'application/xml'),
    t('yaml',        'YAML',             'yaml',     'text/plain'),
]

TEMPEL_EDIT_AGE = 5 # minutes

