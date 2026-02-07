import logging
from logging import Formatter

logger = logging.getLogger('evo-sim')

logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler()
handler.setLevel(logging.DEBUG)
formatter = Formatter(
    '%(levelname)s:     ' +
    '%(asctime)s -- %(module)s.%(funcName)s:%(lineno)d' +
    '-- %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
