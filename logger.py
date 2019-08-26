import logging
import os
from logging.handlers import RotatingFileHandler
from config import ROOT

logger = logging.getLogger('collector')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(
    os.path.join(ROOT, 'logs/collector.log'),
    maxBytes=10000000, backupCount=5,
    encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)