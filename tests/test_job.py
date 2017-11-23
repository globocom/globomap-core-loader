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
import unittest

from api.database import init_db, destroy_db
from api.job.models import Job, JobError


class TestJob(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        init_db()

    @classmethod
    def tearDownClass(self):
        destroy_db()

    def setUp(self):
        init_db()

    def tearDown(self):
        destroy_db()

    def test_increment_success_count(self):
        job = Job('driver', 1)
        job.increment_success_count()
        self.assertEqual(1, job.success_count)

    def test_is_completed(self):
        job = Job('driver', 1)
        job.increment_success_count()
        self.assertTrue(job._is_completed())

    def test_not_completed(self):
        job = Job('driver', 1)
        self.assertFalse(job._is_completed())

    def test_add_error(self):
        job = Job('driver', 1)
        job.add_error(JobError('', '', 200))
        self.assertEqual(1, job.error_count)

    def test_save(self):
        job = Job('driver', 1)
        job.save()
        self.assertFalse(job.completed)
        self.assertIsNotNone(Job.find_by_uuid(job.uuid))

    def test_save_completed(self):
        job = Job('driver', 1)
        job.increment_success_count()
        job.save()
        self.assertTrue(job.completed)
        self.assertIsNotNone(Job.find_by_uuid(job.uuid))

    def test_get_date_time(self):
        pass