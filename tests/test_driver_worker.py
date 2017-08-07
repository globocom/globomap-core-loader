from mock import MagicMock, Mock
from loader.globomap import GloboMapException
from loader.loader import DriverWorker
from tests.util import open_json
import unittest


class TestDriverWorker(unittest.TestCase):

    def test_sync_updates(self):
        updates = open_json('tests/json/driver/driver_output_create.json')
        driver_mock = self._mock_driver(updates)
        globomap_client_mock = MagicMock()

        worker = DriverWorker(globomap_client_mock, driver_mock, None)
        worker._sync_updates()

        driver_mock.updates.assert_called_once_with(1)
        globomap_client_mock.update_element_state.assert_called_once_with('CREATE', 'collections', 'vip', updates[0]['element'])

    def test_sync_updates_expected_exception(self):
        updates = open_json('tests/json/driver/driver_output_create.json')
        driver_mock = self._mock_driver(updates)
        globomap_client_mock = self._mock_globomap_client(GloboMapException())
        exception_handler = MagicMock()

        worker = DriverWorker(globomap_client_mock, driver_mock, exception_handler)
        worker._sync_updates()

        driver_mock.updates.assert_called_once_with(1)
        globomap_client_mock.update_element_state.assert_called_once_with('CREATE', 'collections', 'vip', updates[0]['element'])
        exception_handler.handle_exception.assert_called_once_with(updates[0])

    def _mock_driver(self, return_value):
        driver_mock = Mock()
        generator_mock = Mock()
        generator_mock.__iter__ = Mock(return_value = iter([return_value]))
        driver_mock.updates.return_value = generator_mock
        return driver_mock

    def _mock_globomap_client(self, exception):
        driver_mock = Mock()
        driver_mock.update_element_state.side_effect = exception
        return driver_mock
