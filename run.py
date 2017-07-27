#!/usr/bin/env python
import logging

from loader.loader import CoreLoader

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(asctime)s %(threadName)s %(levelname)s %(message)s')
    CoreLoader().load()
