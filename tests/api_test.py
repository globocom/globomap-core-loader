"""
   Copyright 2018 Globo.com

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
import json
import unittest

from mock import Mock
from mock import patch

from globomap_core_loader.api.app import create_app
from globomap_core_loader.api.database import destroy_db
from globomap_core_loader.api.database import init_db
from globomap_core_loader.api.job.models import Job
from globomap_core_loader.api.job.models import JobError
from tests.util import open_json


class ApiTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app().test_client()

    @classmethod
    def setUpClass(cls):
        init_db()

    @classmethod
    def tearDownClass(self):
        destroy_db()

    def test_send_updates(self):
        rabbit_mock = self._mock_rabbitmq_client(True)
        updates = [open_json('tests/json/driver/driver_output_create.json')]
        response = self.app.post(
            '/v1/updates',
            data=json.dumps(updates),
            headers={'Content-Type': 'application/json'}
        )

        response_json = json.loads(response.data)
        self.assertEqual(202, response.status_code)
        self.assertEqual('Location', response.headers[2][0])
        self.assertEqual('http://localhost/v1/updates/job/%s' %
                         response_json['jobid'], response.headers[2][1])
        self.assertEqual('Updates published successfully',
                         response_json['message'])
        self.assertEqual(1, rabbit_mock.post_message.call_count)
        self.assertEqual(1, rabbit_mock.confirm_publish.call_count)
        self.assertIsNotNone(Job.find_by_uuid(response_json['jobid']))

    def test_send_updates_no_updates_found(self):
        rabbit_mock = self._mock_rabbitmq_client(True)
        response = self.app.post(
            '/v1/updates',
            data=json.dumps([]),
            headers={'Content-Type': 'application/json'}
        )

        self.assertEqual(400, response.status_code)
        self.assertEqual('Invalid empty request',
                         json.loads(response.data)['errors'])
        self.assertEqual(0, rabbit_mock.post_message.call_count)

    def test_send_updates_expected_status_400(self):
        response = self.app.post(
            '/v1/updates',
            data=json.dumps({'key': 'wrong input'}),
            headers={'Content-Type': 'application/json'}
        )

        self.assertEqual(400, response.status_code)

    def test_send_updates_expected_status_500(self):
        rabbit_mock = self._mock_rabbitmq_client(Exception())
        updates = [open_json('tests/json/driver/driver_output_create.json')]
        response = self.app.post(
            '/v1/updates',
            data=json.dumps(updates),
            headers={'Content-Type': 'application/json'}
        )

        self.assertEqual(500, response.status_code)
        self.assertEqual(1, rabbit_mock.post_message.call_count)
        self.assertEqual(1, rabbit_mock.discard_publish.call_count)

    def test_get_job(self):
        job = Job('driver_name', 1)
        job.add_error(JobError('{"a": "1"}', '{"a": "1"}', 400))
        job.save()

        response = self.app.get(
            '/v1/updates/job/%s' % job.uuid,
            headers={'Content-Type': 'application/json'}
        )
        job_json = json.loads(response.data)

        self.assertEqual(200, response.status_code)
        self.assertEqual(job.uuid, job_json['uuid'])
        self.assertEqual('driver_name', job_json['driver'])
        self.assertEqual(0, job_json['successful_update_count'])
        self.assertEqual(1, job_json['error_update_count'])
        self.assertEqual(True, job_json['completed'])
        self.assertEqual(1, len(job_json['errors']))

    def _mock_rabbitmq_client(self, data=None):
        rabbit_mq_mock = patch(
            'globomap_core_loader.api.facade.LoaderAPIFacade._get_rabbit_mq_client').start()
        post_message_mock = Mock()
        rabbit_mq_mock.return_value = post_message_mock
        if type(data) is bool:
            post_message_mock.post_message.return_value = data
        else:
            post_message_mock.post_message.side_effect = data
        return post_message_mock
