import logging

from ZoopAPIWrapper.constants import LOG_LEVEL


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=LOG_LEVEL
)

logger = logging.getLogger('ZoopAPIWrapper')
