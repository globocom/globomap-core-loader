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
