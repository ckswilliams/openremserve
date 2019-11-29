LOCAL_SETTINGS = True
from settings import *


# Choose your database and fill in the details below. If testing, you
# can use the sqlite3 database as it doesn't require any further configuration
# A Windows example path might be: 'C:/Users/myusername/Documents/OpenREM/openrem.db'
# Note, forward slashes are used in the config files, even for Windows.

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',  # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'openremdb', # Or path to database file if using sqlite3.
        'USER': 'openremuser',                              # Not used with sqlite3.
        'PASSWORD': 'nopasswordhere',                          # Not used with sqlite3.
        'HOST': 'postgres',                              # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '5432',                              # Set to empty string for default. Not used with sqlite3.
    }
}

# Celery settings
BROKER_URL = 'amqp://guest:guest@rabbitmq//'

CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_DEFAULT_QUEUE = 'default'

CELERYD_PREFETCH_MULTIPLIER = 1

BROKER_MANAGER_URL = 'http://rabbitmq'
BROKER_MANAGER_PORT = 15672
FLOWER_URL = 'http://flower'
FLOWER_PORT = 5555

CELERYBEAT_SCHEDULE = {
    'trigger-dicom-keep-alive': {
        'task': 'remapp.netdicom.keepalive.keep_alive',
        'schedule': crontab(minute='*/1'),
        'options': {'expires': 10},  # expire if not run ten seconds after being scheduled
    },
}

# Absolute filesystem path to the directory that will hold xlsx and csv
# exports patient size import files
# Linux example: "/var/openrem/media/"
# Windows example: "C:/Users/myusername/Documents/OpenREM/media/"
MEDIA_ROOT = '/var/dose/media'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = '/var/dose/static'

# You should generate a new secret key. Make this unique, and don't
# share it with anybody. See the docs.
# Original - SECRET_KEY = 'hmj#)-$smzqk*=wuz9^a46rex30^$_j$rghp+1#y&amp;i+pys5b@$'
SECRET_KEY = 'hmj#)-$smzqk*=wuz9^a46rex30^$_j$rghp+1#y&amp;i+pys5b@$'

# Debug mode is now set to False by default. If you need to troubleshoot, can turn it back on here:
#DEBUG = True

# Set the domain name that people will use to access your OpenREM server.
# This is required if the DEBUG mode is set to False (default)
# Example: '.doseserver.' or '10.23.123.123'. A dot before a name allows subdomains, a dot after allows for FQDN eg
# doseserver.ad.trust.nhs.uk. Alternatively, use '*' to remove this security feature if you handle it in other ways.
ALLOWED_HOSTS = [
    '*',
]

# Logging configuration
# Set the log file location. The example places the log file in the media directory. Change as required - on linux
# systems you might put these in a subdirectory of /var/log/. If you want all the logs in one file, set the filename
# to be the same for each one.
import os
logfilename = os.path.join(MEDIA_ROOT, "openrem.log")
qrfilename = os.path.join(MEDIA_ROOT, "openrem_qr.log")
storefilename = os.path.join(MEDIA_ROOT, "openrem_store.log")
extractorfilename = os.path.join(MEDIA_ROOT, "openrem_extractor.log")

LOGGING['handlers']['file']['filename'] = logfilename          # General logs
LOGGING['handlers']['qr_file']['filename'] = qrfilename        # Query Retrieve SCU logs
LOGGING['handlers']['store_file']['filename'] = storefilename  # Store SCP logs
LOGGING['handlers']['extractor_file']['filename'] = extractorfilename  # Extractor logs

# Set log message format. Options are 'verbose' or 'simple'. Recommend leaving as 'verbose'.
LOGGING['handlers']['file']['formatter'] = 'verbose'        # General logs
LOGGING['handlers']['qr_file']['formatter'] = 'verbose'     # Query Retrieve SCU logs
LOGGING['handlers']['store_file']['formatter'] = 'verbose'  # Store SCP logs
LOGGING['handlers']['extractor_file']['formatter'] = 'verbose'  # Extractor logs

# Set the log level. Options are 'DEBUG', 'INFO', 'WARNING', 'ERROR', and 'CRITICAL', with progressively less logging.
LOGGING['loggers']['remapp']['level'] = 'INFO'                    # General logs
LOGGING['loggers']['remapp.netdicom.qrscu']['level'] = 'INFO'     # Query Retrieve SCU logs
LOGGING['loggers']['remapp.netdicom.storescp']['level'] = 'INFO'  # Store SCP logs
LOGGING['loggers']['remapp.extractors.ct_toshiba']['level'] = 'INFO'  # Toshiba RDSR creation extractor logs

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Africa/Niamey'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'
