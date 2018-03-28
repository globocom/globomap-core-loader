#!/usr/bin/env python
from migrate.versioning.shell import main

from globomap_core_loader.settings import SQLALCHEMY_DATABASE_URI

if __name__ == '__main__':
    main(url=SQLALCHEMY_DATABASE_URI, repository='./migrations/')
