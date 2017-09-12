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
import logging
import os
from logging.handlers import RotatingFileHandler

from api.app import create_app

if __name__ == '__main__':
    handler = RotatingFileHandler(
        'globomap-loader-api.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.DEBUG)
    logging.basicConfig(
        filename='globomap-loader-api.log',
        level=logging.DEBUG,
        format='%(asctime)s %(threadName)s %(levelname)s %(message)s'
    )

    app = create_app()
    app.logger.addHandler(handler)
    app.run('0.0.0.0', int(os.getenv('PORT', '5000')), debug=True)
