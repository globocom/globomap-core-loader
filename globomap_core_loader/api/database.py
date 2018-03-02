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
from sqlite3 import dbapi2 as sqlite

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from globomap_core_loader.settings import DATABASE_POOL_OVERFLOW
from globomap_core_loader.settings import DATABASE_POOL_RECYCLE
from globomap_core_loader.settings import DATABASE_POOL_SIZE
from globomap_core_loader.settings import SQLALCHEMY_DATABASE_URI

if os.getenv('ENV') == 'test':
    engine = create_engine('sqlite+pysqlite:///file.db', module=sqlite)
else:
    engine = create_engine(SQLALCHEMY_DATABASE_URI, convert_unicode=True,
                           pool_size=DATABASE_POOL_SIZE,
                           pool_recycle=DATABASE_POOL_RECYCLE,
                           max_overflow=DATABASE_POOL_OVERFLOW)

session_maker = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

Base = declarative_base()
Session = scoped_session(session_maker)


def init_db():
    import globomap_core_loader.api.job.models
    Base.metadata.create_all(bind=engine)


def destroy_db():
    Base.metadata.drop_all(bind=engine)
