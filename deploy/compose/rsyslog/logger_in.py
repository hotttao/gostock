import logging
from rfc5424logging import Rfc5424SysLogHandler

logger = logging.getLogger('syslogtest')
logger.setLevel(logging.INFO)

sh = Rfc5424SysLogHandler(
    address=('127.0.0.1', 514),
    msg_as_utf8=False,
    hostname="otherserver",
    appname="my_wonderfull_app",
    procid=555,
    structured_data={'sd_id_1': {'key1': 'value1'}},
    enterprise_id=32473
)
logger.addHandler(sh)

msg_type = 'interesting'
extra = {
    'msgid': 'some_unique_msgid',
    'structured_data': {
        'sd_id2': {'key2': 'value2', 'key3': 'value3'}
    }
}
logger.info('This is an %s message', msg_type, extra=extra)
