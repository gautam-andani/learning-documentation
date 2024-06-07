import os
import logging
import logging.config

LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters':{
        'standard': {
            'format': '%(asctime)s [%(levelname)s] %(name)s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'standard',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': 'app.log',
            'formatter': 'standard',
            'when': 'midnight',
            'backupCount': 30,       # logs of last 30 days
        },
    },
    'loggers': {
        '': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'werkzeug': {  # Configure the werkzeug logger
            'handlers': ['console'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'app': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
def setup_logging():
    if os.getenv('FLASK_ENV') == 'testing':
        LOGGING_CONFIG['handlers']['file']['filename'] = 'test_app.log'
        
    logging.config.dictConfig(LOGGING_CONFIG)