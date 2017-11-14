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
from mock import MagicMock, Mock
from api.database import destroy_db
from api.database import init_db
from api.job.models import Job
from loader.globomap import GloboMapException
from loader.loader import DriverWorker
from tests.util import open_json
import unittest


class TestDriverWorker(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()

    @classmethod
    def tearDownClass(self):
        destroy_db()

    def test_sync_updates(self):
        update = open_json('tests/json/driver/driver_output_create.json')
        globomap_client_mock = MagicMock()

        DriverWorker(globomap_client_mock, Mock(), None)._process_update(update)
        globomap_client_mock.update_element_state.assert_called_once_with(
            'CREATE', 'collections', 'vip', update['element'], None
        )

    def test_sync_updates_expected_exception(self):
        update = open_json('tests/json/driver/driver_output_create.json')
        globomap_client_mock = self._mock_globomap_client(
            GloboMapException(400, {"errors": "error msg"})
        )
        exception_handler = MagicMock()

        DriverWorker(globomap_client_mock, Mock(), exception_handler)._process_update(update)

        globomap_client_mock.update_element_state.assert_called_once_with(
            'CREATE', 'collections', 'vip', update['element'], None
        )
        exception_handler.handle_exception.assert_called_once_with('Mock', update)
        self.assertEqual(400, update['status'])
        self.assertEqual({"errors": "error msg"}, update['error_msg'])

    def test_update_job_error(self):
        job = Job(1).save()
        worker = DriverWorker(None, None, None)
        response_mock = Mock()
        response_mock.response = '{"message": "error"}'
        response_mock.status_code = 400
        worker.update_job_error(job.uuid, {}, response_mock)

        job = Job.find_by_uuid(job.uuid)
        self.assertTrue(job.completed)
        self.assertEquals(1, job.error_count)

    def test_update_job_success(self):
        job = Job(1).save()
        worker = DriverWorker(None, None, None)
        worker.update_job_success(job.uuid)

        job = Job.find_by_uuid(job.uuid)
        self.assertTrue(job.completed)

    def _mock_driver(self, return_value):
        driver_mock = Mock()
        driver_mock.updates.side_effect = [return_value, []]
        return driver_mock

    def _mock_globomap_client(self, exception):
        globomap_mock = Mock()
        globomap_mock.update_element_state.side_effect = exception
        return globomap_mock
