import logging
import logging.config

log_settings = {
    'version': 1,
    'formatters': {
        'console': {
            'format': '[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s',
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'syslog': {
            'level': 'INFO',
            'class': 'rfc5424logging.handler.Rfc5424SysLogHandler',
            'address': ('127.0.0.1', 514),
            'enterprise_id': 32473,
            'structured_data': {'sd_id': {'key1': 'value1'}},
        },
    },
    'loggers': {
        'syslogtest': {
            'handlers': ['console', 'syslog'],
            'level': 'DEBUG',
        },
    }
}
logging.config.dictConfig(log_settings)
print('start logger')
logger = logging.getLogger('syslogtest')

logger.info('This message appears on console and is sent to syslog')
logger.debug('This debug message appears on console only')
