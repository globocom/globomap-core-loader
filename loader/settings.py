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
    {'package': 'driver.generic', 'class': 'GenericDriver', 'factor': 5},
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
    'updates': 'api/specs/updates.json',
}
