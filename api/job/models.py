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
import uuid
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.schema import ForeignKey
from api.database import db_session, Base


class Job(Base):

    __tablename__ = 'job'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(50), nullable=False)
    updates_count = Column(Integer, nullable=False)
    success_count = Column(Integer, nullable=False)
    completed = Column(Boolean, nullable=False)
    date_created = Column(DateTime, nullable=False)
    errors = relationship(
        'JobError', backref='Job', lazy=True, passive_deletes=True
    )

    def __init__(self, updates_count):
        self.uuid = str(uuid.uuid4())
        self.date_created = datetime.now()
        self.updates_count = updates_count
        self.completed = False
        self.success_count = 0

    def increment_success_count(self):
        self.success_count += 1

    @property
    def error_count(self):
        return len(self.errors) if self.errors else 0

    def _is_completed(self):
        return self.error_count + self.success_count == self.updates_count

    def add_error(self, job_error):
        self.errors.append(job_error)

    def save(self):
        db_session.add(self)
        if self._is_completed():
            self.completed = True
        db_session.commit()
        return self

    @staticmethod
    def find_by_uuid(uuid):
        return db_session.query(Job).filter_by(uuid=uuid).first()

    @property
    def date_time(self):
        return self.date_created.strftime('%d/%m/%Y %H:%M:%S')


class JobError(Base):

    __tablename__ = 'job_error'

    id = Column(Integer, primary_key=True)
    uuid = Column(String(50), nullable=False)
    request_body = Column(String(1024), nullable=False)
    response = Column(String(1024), nullable=False)
    status_code = Column(String(3), nullable=True)
    job_id = Column(Integer, ForeignKey('job.id', ondelete='CASCADE'),
                    nullable=False)

    def __init__(self, request_body, response, status_code):
        self.uuid = str(uuid.uuid4())
        self.request_body = request_body
        self.response = response
        self.status_code = status_code

    @property
    def date_time(self):
        return self.date.strftime('%d/%m/%Y %H:%M:%S')
