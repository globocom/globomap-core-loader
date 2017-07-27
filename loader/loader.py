import importlib
import logging
from threading import Thread
from globomap import GloboMapClient, GloboMapException
from settings import GLOBOMAP_API_ADDRESS, DRIVERS


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
                self.log.error("Cannot load driver '%s' attribute not found" % driver_class)
            except ImportError:
                self.log.error("Cannot load driver '%s'. Module not found %s" % (driver_class, package))

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

    def _sync_updates(self):
        for update in self.driver.updates():
            try:
                update = update[0]
                self.globomap_client.update_element_state(update['action'], update['type'], update['element'])
            except GloboMapException:
                self.log.exception("Error updating element %s" % update)
                self.exception_handler.handle_exception(update)


class UpdateExceptionHandler(object):

    def handle_exception(self, update):
        pass # TODO: return message to the driver OR send to a queue to be handled later on
