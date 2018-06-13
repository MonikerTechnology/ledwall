import log
import os

file = str(os.path.basename(__file__))
log.warning(file,"THis is a test of warning")

log.info(file,"This is info")

log.header(file,"header message")