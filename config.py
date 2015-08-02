# coding : utf-8

import logging
import logging.handlers

# IE SETTINGS

USER_AGENTS = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10.7; rv:11.0) Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100 101 Firefox/22.0',
               'Mozilla/5.0 (Windows NT 6.1; rv:11.0) Gecko/20100101 Firefox/11.0',
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_4) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5',
               'Mozilla/5.0 (Windows; Windows NT 6.1) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.46 Safari/536.5',)

# setting logging

LOG_FILE = 'tst.log'

formatter = logging.Formatter(
    '[%(asctime)s %(levelname)s %(filename)s:%(lineno)d]: %(message)s'
)

# initialize handler
# handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024*1024, backupCount=5)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
logger = logging.getLogger('cba')
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)
