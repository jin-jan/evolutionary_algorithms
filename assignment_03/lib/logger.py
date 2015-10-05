import sys
import types
import os
import logging
import inspect

INFO = 50
RESULTBF = 40
RESULTAF = 30
DEBUG = 20

LOG_FORMAT_GEN = ('[%(asctime)s][%(levelname)s]:%(message)s')
LOG_FORMAT_INFO = ('[%(asctime)s][%(levelname)s]:%(message)s')
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"
LOG_FILENAME = 'assign3.log'

if hasattr(sys, 'frozen'):
    _SRCFILE = "logging%s__init__%s" % (os.sep, __file__[-4:])
elif (__file__[-4:]).lower() in ['.pyc', '.pyo']:
    _SRCFILE = __file__[:-4] + '.py'
else:
    _SRCFILE = __file__

_SRCFILE = os.path.normcase(_SRCFILE)

current_frame = lambda: inspect.stack()[3][0]


def caller():
    """
    Find the stack frame of the caller so that we can note the source
    file name, line number and function name.

    Needed to override this function because Logger class returns the first
    function in the chain of callers which doesn't belong to the current module.
    """
    current_f = current_frame()
    if current_f is not None:
        current_f = current_f.f_back
    return_value = "(unknown file)", 0, "(unknown function)"
    while hasattr(current_f, "f_code"):
        current_code = current_f.f_code
        filename = os.path.normcase(current_code.co_filename)
        if filename == _SRCFILE:
            current_f = current_f.f_back
            continue
        return_value = (filename, current_f.f_lineno,
                        current_code.co_name)
        break
    return return_value


class CELogger(logging.Logger):

    def __init__(self, name):
        logging.Logger.__init__(self, name)

    def info(self, msg, *args, **kwargs):
        """Log 'msg % args' with severity 'STATUS' = 50."""
        self._log(INFO, msg, args, **kwargs)

    def rbf(self, msg, *args, **kwargs):
        """Log 'msg % args' with severity 'INFO' = 40."""
        self._log(RESULTBF, msg, args, **kwargs)

    def raf(self, msg, *args, **kwargs):
        """Log 'msg % args' with severity 'DETAIL' = 30."""
        self._log(RESULTAF, msg, args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        """Log 'msg % args' with severity 'DEBUG' = 10."""
        self._log(DEBUG, msg, args, **kwargs)

    def _log(self, level, msg, args, exc_info=None, extra=None):
        """
        Low-level logging routine which creates a LogRecord and then calls
        all the handlers of this logger to handle the record.
        """
        if _SRCFILE:
            try:
                file_name, lno, func = caller()
            except ValueError:
                file_name, lno, func = "(unknown file)", 0, "(unknown function)"
        else:
            file_name, lno, func = "(unknown file)", 0, "(unknown function)"
        if exc_info:
            if not isinstance(exc_info, types.TupleType):
                exc_info = sys.exc_info()
        record = self.makeRecord(self.name, level, file_name,
                                 lno, msg, args, exc_info, func, extra)
        self.handle(record)


logging.setLoggerClass(CELogger)

LOG = logging.getLogger("ce_logger")

LOG.propagate = False
LOG.setLevel(DEBUG)

needRoll = os.path.isfile(LOG_FILENAME)

logging.addLevelName(INFO, "Info")
logging.addLevelName(RESULTBF, "ResultBF")
logging.addLevelName(RESULTAF, "ResultAF")
logging.addLevelName(DEBUG, "Debug")
STDOUT_HANDLER = logging.StreamHandler(sys.stdout)
STDOUT_HANDLER.setLevel(INFO)
FILE_HANDLER = logging.FileHandler(LOG_FILENAME, 'w')
FILE_HANDLER.setLevel(DEBUG)
STDOUT_FMT = logging.Formatter(fmt=LOG_FORMAT_INFO,
                               datefmt=LOG_DATE_FORMAT)
FILE_FMT = logging.Formatter(fmt=LOG_FORMAT_GEN,
                             datefmt=LOG_DATE_FORMAT)
STDOUT_HANDLER.setFormatter(STDOUT_FMT)
FILE_HANDLER.setFormatter(FILE_FMT)
LOG.addHandler(STDOUT_HANDLER)
LOG.addHandler(FILE_HANDLER)
