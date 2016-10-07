import sys

import logging
from logging import StreamHandler

handler = StreamHandler(stream=sys.stdout)
handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s:%(msecs)d-%(levelname)s-%(module)s:%(lineno)d:%(message)s')
handler.setFormatter(formatter)
log = logging.getLogger(__name__)
log.addHandler(handler)
log.setLevel(logging.INFO)
