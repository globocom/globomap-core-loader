import os

GLOBOMAP_API_ADDRESS = os.getenv('GLOBOMAP_API_ADDRESS')
GLOBOMAP_RMQ_USER = os.getenv('GLOBOMAP_RMQ_USER')
GLOBOMAP_RMQ_PASSWORD = os.getenv('GLOBOMAP_RMQ_PASSWORD')
GLOBOMAP_RMQ_HOST = os.getenv('GLOBOMAP_RMQ_HOST')
GLOBOMAP_RMQ_PORT = int(os.getenv('GLOBOMAP_RMQ_PORT', 5672))
GLOBOMAP_RMQ_VIRTUAL_HOST = os.getenv('GLOBOMAP_RMQ_VIRTUAL_HOST')
GLOBOMAP_RMQ_QUEUE_NAME = os.getenv('GLOBOMAP_RMQ_QUEUE_NAME')

DRIVERS = [
    {'package': 'globomap_driver_napi.driver','class': 'Napi'},
    {'package': 'driver.generic','class': 'GenericDriver'},
]