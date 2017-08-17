import os

DRIVER_FETCH_INTERVAL = int(os.getenv('DRIVER_FETCH_INTERVAL', 60))
DRIVER_NUMBER_OF_UPDATES = int(os.getenv('DRIVER_NUMBER_OF_UPDATES', 1))
GLOBOMAP_API_ADDRESS = os.getenv('GLOBOMAP_API_ADDRESS')
GLOBOMAP_RMQ_USER = os.getenv('GLOBOMAP_RMQ_USER')
GLOBOMAP_RMQ_PASSWORD = os.getenv('GLOBOMAP_RMQ_PASSWORD')
GLOBOMAP_RMQ_HOST = os.getenv('GLOBOMAP_RMQ_HOST')
GLOBOMAP_RMQ_PORT = int(os.getenv('GLOBOMAP_RMQ_PORT', 5672))
GLOBOMAP_RMQ_VIRTUAL_HOST = os.getenv('GLOBOMAP_RMQ_VIRTUAL_HOST')
GLOBOMAP_RMQ_QUEUE_NAME = os.getenv('GLOBOMAP_RMQ_QUEUE_NAME')
GLOBOMAP_RMQ_EXCHANGE = os.getenv('GLOBOMAP_RMQ_EXCHANGE')
GLOBOMAP_RMQ_ERROR_EXCHANGE = os.getenv('GLOBOMAP_RMQ_ERROR_EXCHANGE')
GLOBOMAP_RMQ_KEY = os.getenv('GLOBOMAP_RMQ_BINDING_KEY', 'globomap.updates')

DRIVERS = [
    {'package': 'driver.generic', 'class': 'GenericDriver'},
    {'package': 'globomap_driver_napi.driver', 'class': 'Napi'},
    {
        'package': 'globomap_driver_acs.driver', 'class': 'Cloudstack',
        'params': {
            'env': 'CTA'
        }
    },
    {
        'package': 'globomap_driver_acs.driver', 'class': 'Cloudstack',
        'params': {
            'env': 'CME'
        }
    }
]
