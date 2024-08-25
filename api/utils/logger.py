import logging
import os

logger = logging.getLogger("grateful")
_handler = logging.StreamHandler()
_formatter = logging.Formatter("%(levelname)s %(message)s")
_handler.setFormatter(_formatter)

logger.addHandler(_handler)

if os.environ.get("DEBUG", False):
    LEVEL = 10
else:
    LEVEL = 20

logger.setLevel(level=LEVEL)
logger.debug("** DEBUGGER ACTIVE **")
