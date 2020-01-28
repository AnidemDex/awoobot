#!/usr/bin/env python3
import logging
log = logging.getLogger(__name__)

try:
    import awoobot
    awoobot.start()
except Exception as error:
    log.exception("Algo ocurrio")
