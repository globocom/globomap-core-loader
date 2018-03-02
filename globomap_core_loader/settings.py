"""
   Copyright 2017 Globo.com

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""
import os

DRIVER_FETCH_INTERVAL = int(os.getenv('DRIVER_FETCH_INTERVAL', 60))

GLOBOMAP_API_ADDRESS = os.getenv('GLOBOMAP_API_ADDRESS')

GLOBOMAP_API_URL = os.getenv('GLOBOMAP_API_URL')

GLOBOMAP_RMQ_USER = os.getenv('GLOBOMAP_RMQ_USER')
GLOBOMAP_RMQ_PASSWORD = os.getenv('GLOBOMAP_RMQ_PASSWORD')
GLOBOMAP_RMQ_HOST = os.getenv('GLOBOMAP_RMQ_HOST')
GLOBOMAP_RMQ_PORT = int(os.getenv('GLOBOMAP_RMQ_PORT', 5672))
GLOBOMAP_RMQ_VIRTUAL_HOST = os.getenv('GLOBOMAP_RMQ_VIRTUAL_HOST')
GLOBOMAP_RMQ_QUEUE_NAME = os.getenv('GLOBOMAP_RMQ_QUEUE_NAME')
GLOBOMAP_RMQ_EXCHANGE = os.getenv('GLOBOMAP_RMQ_EXCHANGE')
GLOBOMAP_RMQ_ERROR_EXCHANGE = os.getenv('GLOBOMAP_RMQ_ERROR_EXCHANGE')
GLOBOMAP_RMQ_KEY = os.getenv('GLOBOMAP_RMQ_BINDING_KEY', 'globomap.updates')

DATABASE_POOL_SIZE = os.getenv('DATABASE_POOL_SIZE', 20)
DATABASE_POOL_OVERFLOW = os.getenv('DATABASE_POOL_OVERFLOW', 10)
DATABASE_POOL_RECYCLE = os.getenv('DATABASE_POOL_RECYCLE', 120)
SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
SCHEDULER_FREQUENCY_EXEC = os.getenv('SCHEDULER_FREQUENCY_EXEC')

# Redis
REDIS_SENTINEL_ENDPOINT_SIMPLE = os.getenv('REDIS_SENTINEL_ENDPOINT_SIMPLE')
REDIS_SENTINEL_SERVICE_NAME = os.getenv('REDIS_SENTINEL_SERVICE_NAME')
REDIS_SENTINEL_PASSWORD = os.getenv('REDIS_SENTINEL_PASSWORD')
REDIS_SENTINELS_PORT = os.getenv('REDIS_SENTINELS_PORT')
REDIS_SENTINELS = os.getenv('REDIS_SENTINELS')
REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD')

# Keystone
KEYSTONE_AUTH_ENABLE = os.getenv('KEYSTONE_AUTH_ENABLE')
KEYSTONE_AUTH_URL = os.getenv('KEYSTONE_AUTH_URL')
KEYSTONE_TENANT_NAME = os.getenv('KEYSTONE_TENANT_NAME')

DRIVERS = [
    {'package': 'globomap_core_loader.driver.generic',
        'class': 'GenericDriver', 'factor': 5},
    {'package': 'globomap_driver_napi.driver', 'class': 'Napi', 'factor': 1},
    {
        'package': 'globomap_driver_acs.driver', 'class': 'Cloudstack',
        'params': {
            'env': 'CTA'
        }, 'factor': 1
    },
    {
        'package': 'globomap_driver_acs.driver', 'class': 'Cloudstack',
        'params': {
            'env': 'DEV'
        }, 'factor': 1
    },
    {
        'package': 'globomap_driver_acs.driver', 'class': 'Cloudstack',
        'params': {
            'env': 'CME'
        }, 'factor': 1
    }
]

SPECS = {
    'updates': 'globomap_core_loader/api/specs/updates.json',
}

LOADER_UPDATE = 'globomap_loader_update'

# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'formatters': {
#         'verbose': {
#             'format': 'U:%%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d msg"%(message)s" U:%(request_id)-6s, '
#                       'P:%(request_path)-8s'
#         }
#     },
#     # 'filters': {
#     #     'special': {
#     #         '()': 'api.extra_logging.filters.StaticFieldFilter',
#     #     },
#     #     'requestfilter': {
#     #         '()': 'api.extra_logging.filters.RequestFilter',
#     #     },
#     #     'user_filter': {
#     #         '()': 'api.extra_logging.filters.ExtraLoggingFilter',
#     #     }
#     # },
#     'handlers': {
#         'default': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'stream': 'ext://sys.stdout',
#             'formatter': 'verbose',
#             # 'filters': ['special', 'requestfilter', 'user_filter'],
#         }
#     },
#     'loggers': {
#         'api': {
#             'handlers': ['default'],
#             'level': 'DEBUG',
#             'propagate': True
#         },
#         'werkzeug': {'propagate': True},
#     }
# }
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d ' +
            '%(thread)d %(message)s'
        }
    },
    'handlers': {
        'default': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'stream': 'ext://sys.stdout',
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'api': {
            'handlers': ['default'],
            'level': 'DEBUG',
            'propagate': True
        },
        'werkzeug': {'propagate': True},
    }
}
