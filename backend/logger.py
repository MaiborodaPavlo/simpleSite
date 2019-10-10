import logging
from functools import wraps
import inspect
import sys


class Logger:
    instance = None
    LOG_FILE = '.log'

    def __new__(cls):
        if cls.instance is None:
            cls.instance = super(Logger, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.logger = logging.getLogger(__name__)

        if not self.logger.hasHandlers():
            fh = logging.FileHandler(self.LOG_FILE)
            fmt = '%(asctime)s [%(levelname)s] %(message)s'
            formatter = logging.Formatter(fmt)
            fh.setFormatter(formatter)

            sh = logging.StreamHandler(sys.stdout)
            sh.setFormatter(formatter)

            self.logger.addHandler(fh)
            self.logger.addHandler(sh)

    def __getattr__(self, name):
        if name in ['critical', 'error', 'warning', 'info', 'debug']:

            self.logger.setLevel(name.upper())

            def wrapper(msg):
                method = inspect.stack()[1][3]
                frm = inspect.stack()[1][0]
                if 'self' in frm.f_locals:
                    clsname = frm.f_locals['self'].__class__.__name__
                    method = clsname + '.' + method
                if not method.startswith('<'):
                    method += '()'
                msg = ':'.join((method, str(frm.f_lineno), msg))

                return getattr(self.logger, name)(msg)

            return wrapper

        return super(Logger, self).__getattr__(name)


def errors_logger(method):
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        logger_ = Logger()
        try:
            return method(self, *args, **kwargs)
        except Exception as ex:
            msg = f'Exception in {method.__name__}. {ex.__class__}: {ex}'
            logger_.error(msg)
            raise

    return wrapper


def class_logger(decorator=errors_logger):
    def decorate(cls):
        for attr in cls.__dict__:
            if callable(getattr(cls, attr)) and not attr.startswith('_'):
                setattr(cls, attr, decorator(getattr(cls, attr)))
        return cls
    return decorate


logger = Logger()
