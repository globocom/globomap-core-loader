import importlib
import json
import logging
import time
from threading import Thread
from globomap import GloboMapClient, GloboMapException
from settings import GLOBOMAP_API_ADDRESS, DRIVERS, GLOBOMAP_RMQ_USER, \
    GLOBOMAP_RMQ_PASSWORD, GLOBOMAP_RMQ_HOST, GLOBOMAP_RMQ_PORT, \
    GLOBOMAP_RMQ_VIRTUAL_HOST, GLOBOMAP_RMQ_ERROR_EXCHANGE, \
    DRIVER_NUMBER_OF_UPDATES, DRIVER_FETCH_INTERVAL
from rabbitmq import RabbitMQClient


class CoreLoader(object):

    log = logging.getLogger(__name__)

    def __init__(self):
        self.log.info("Starting Globmap loader")
        self.drivers = self._load_drivers()
        self.globomap_client = GloboMapClient(GLOBOMAP_API_ADDRESS)

    def load(self):
        for driver in self.drivers:
            DriverWorker(self.globomap_client, driver, UpdateExceptionHandler()).start()

    def _load_drivers(self):
        self.log.info("Loading drivers: %s" % DRIVERS)

        drivers = []
        for driver_config in DRIVERS:
            package = driver_config['package']
            driver_class = driver_config['class']
            try:
                driver_type = getattr(importlib.import_module(package), driver_class)
                if not hasattr(driver_type, 'updates') and not callable(getattr(driver_type, 'updates')):
                    raise AttributeError("Driver '%s' does not implement the method 'updates'" % driver_class)

                drivers.append(driver_type())
                self.log.info("Driver '%s' loaded" % driver_class)
            except AttributeError:
                self.log.exception("Cannot load driver '%s' attribute not found" % driver_class)
            except ImportError:
                self.log.exception("Cannot load driver '%s'. Module not found %s" % (driver_class, package))

        return drivers


class DriverWorker(Thread):

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
                self._sync_updates()
            except Exception:
                self.log.exception("Error syncing updates from driver %s" % self.driver)
            finally:
                time.sleep(DRIVER_FETCH_INTERVAL)

    def _sync_updates(self):
        for updates in self.driver.updates(DRIVER_NUMBER_OF_UPDATES):
            if updates:
                for update in updates:
                    try:
                        self.globomap_client.update_element_state(
                            update['action'], update['type'], update['collection'], update['element']
                        )
                    except GloboMapException:
                        self.log.error("Error calling globo Map API %s" % update)
                        self.exception_handler.handle_exception(update)
                    except Exception:
                        self.log.exception("Unknown error updating element %s" % update)
                        self.exception_handler.handle_exception(update)
            else:
                self.log.debug("No updates found, sleeping for %s secods" % DRIVER_FETCH_INTERVAL)
                time.sleep(DRIVER_FETCH_INTERVAL)


class UpdateExceptionHandler(object):

    def __init__(self):
        self.rabbit_mq = RabbitMQClient(
            GLOBOMAP_RMQ_HOST, GLOBOMAP_RMQ_PORT, GLOBOMAP_RMQ_USER,
            GLOBOMAP_RMQ_PASSWORD, GLOBOMAP_RMQ_VIRTUAL_HOST
        )

    def handle_exception(self, update):
        self.rabbit_mq.post_message(GLOBOMAP_RMQ_ERROR_EXCHANGE, update['type'], json.dumps(update))
