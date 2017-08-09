import logging
import os
from api.app import create_app
from logging.handlers import RotatingFileHandler

if __name__ == '__main__':
    handler = RotatingFileHandler('globomap-loader.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.INFO)
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(threadName)s %(levelname)s %(message)s')

    app = create_app()
    app.logger.addHandler(handler)
    app.run('0.0.0.0', int(os.getenv('PORT', '5000')), debug=True)
