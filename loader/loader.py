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
import importlib
import json
import logging
import time
from threading import Thread
from pika.exceptions import ConnectionClosed

from globomap import GloboMapClient
from globomap import GloboMapException
from settings import DRIVER_FETCH_INTERVAL
from settings import DRIVERS
from settings import GLOBOMAP_API_ADDRESS
from settings import GLOBOMAP_RMQ_ERROR_EXCHANGE
from settings import GLOBOMAP_RMQ_HOST
from settings import GLOBOMAP_RMQ_PASSWORD
from settings import GLOBOMAP_RMQ_PORT
from settings import GLOBOMAP_RMQ_USER
from settings import GLOBOMAP_RMQ_VIRTUAL_HOST
from rabbitmq import RabbitMQClient


class CoreLoader(object):

    log = logging.getLogger(__name__)

    def __init__(self):
        self.log.info('Starting Globmap loader')
        self.drivers = self._load_drivers()
        self.globomap_client = GloboMapClient(GLOBOMAP_API_ADDRESS)

    def load(self):
        for driver in self.drivers:
            DriverWorker(
                self.globomap_client, driver, UpdateExceptionHandler()
            ).start()

    def _load_drivers(self):
        self.log.info('Loading drivers: %s' % DRIVERS)

        drivers = []
        for driver_config in DRIVERS:
            package = driver_config['package']
            driver_class = driver_config['class']
            try:
                driver_instance = self._create_driver_instance(
                    driver_class, package, driver_config.get('params')
                )
                drivers.append(driver_instance)
                self.log.info("Driver '%s' loaded" % driver_class)
            except AttributeError:
                self.log.exception('Cannot load driver %s' % driver_class)
            except ImportError:
                self.log.exception('Cannot load driver %s' % driver_class)
            except Exception:
                self.log.exception(
                    'Unknown error loading driver %s' % driver_config
                )

        return drivers

    def _create_driver_instance(self, driver_class, package, params):
        driver_type = getattr(importlib.import_module(package), driver_class)
        has_update_method = hasattr(driver_type, 'process_updates') and \
            callable(getattr(driver_type, 'process_updates'))

        if not has_update_method:
            raise AttributeError(
                "Driver '%s' doesnt implement 'process_updates'" % driver_class
            )

        if params:
            return driver_type(params)
        else:
            return driver_type()


class DriverWorker(Thread):
    """
    Worker bound to a driver instance that processes all the messages
    provided by the driver and then sleeps for the amount of seconds
    configured by the DRIVER_FETCH_INTERVAL envinroment variable.
    """

    log = logging.getLogger(__name__)

    def __init__(self, globomap_client, driver, exception_handler):
        Thread.__init__(self)
        self.name = driver.__class__.__name__
        self.globomap_client = globomap_client
        self.driver = driver
        self.exception_handler = exception_handler

    def run(self):
        while True:
            try:
                self.driver.process_updates(self._process_update)
            except Exception:
                self.log.exception(
                    'Error syncing updates from driver %s' % self.driver
                )
            finally:
                self.log.debug('No more updates found')
                self.log.debug('Sleeping for %ss' % DRIVER_FETCH_INTERVAL)
                time.sleep(DRIVER_FETCH_INTERVAL)

    def _process_update(self, update):
        try:
            self.globomap_client.update_element_state(
                update['action'],
                update['type'],
                update['collection'],
                update.get('element'),
                update.get('key'),
            )
        except GloboMapException, e:
            self.log.error('Could not process update: %s' % update)
            self.log.error('Status code: %s' % e.status_code)
            self.log.error('Response body: %s' % e.response)
            update['status'] = e.status_code
            update['error_msg'] = e.response
            self.exception_handler.handle_exception(self.name, update)


class UpdateExceptionHandler(object):

    log = logging.getLogger(__name__)

    def __init__(self):
        self._connect_rabbit()

    def _connect_rabbit(self):
        self.rabbit_mq = RabbitMQClient(
            GLOBOMAP_RMQ_HOST, GLOBOMAP_RMQ_PORT, GLOBOMAP_RMQ_USER,
            GLOBOMAP_RMQ_PASSWORD, GLOBOMAP_RMQ_VIRTUAL_HOST
        )

    def handle_exception(self, driver_name, update, retry=True):
        try:
            self.log.debug('Sending failing update to rabbitmq error queue')
            collection = update.get('collection')
            key = 'globomap.error.%s.%s' % (driver_name, collection)
            self.rabbit_mq.post_message(
                GLOBOMAP_RMQ_ERROR_EXCHANGE,
                key,
                json.dumps(update)
            )
        except ConnectionClosed:
            if retry:
                self.log.error("RabbitMQ Connection closed, reconnecting")
                self._connect_rabbit()
                self.handle_exception(driver_name, update, False)
        except Exception as err:
            self.log.exception('Unable to handle exception %s', err)
