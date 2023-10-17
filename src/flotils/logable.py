# -*- coding: UTF-8 -*-
""" Logging utilities """

__author__ = "the01"
__email__ = "jungflor@gmail.com"
__copyright__ = "Copyright (C) 2013-23, Florian JUNG"
__license__ = "MIT"
__version__ = "0.1.7"
__date__ = "2023-11-17"
# Created: 2013-03-03 24:00

import inspect
import logging
from typing import Any, Dict, Optional, Union

from typing_extensions import Protocol

try:
    import colorlog
except ImportError:
    colorlog = None


TIMEFORMAT_DEFAULT = "%Y-%m-%d %H:%M:%S"


# TODO: Switch to build in
class FunctionFilter(logging.Filter):
    """ Add an extra 'function' if not already present """

    def filter(self, record):  # noqa A003
        """ Filter the log record """
        if not hasattr(record, "function"):
            record.function = ""
        else:
            fct = record.function

            if fct and not fct.startswith("."):
                record.function = "." + fct

        return True


class Logable(object):
    """ Class to facilitate clean logging with class/function/id information """

    def __init__(self, settings: Optional[Dict[str, Any]] = None):
        """
        Initialize object

        :param settings: Settings for instance (default: None)
        """
        if settings is None:
            settings = {}

        super().__init__()

        self._id: Optional[Union[str, int]] = settings.get('id', None)
        """ Instance id """

        self._logger = logging.getLogger(self.name)
        """ Internal logger to use """

    @property
    def name(self) -> str:
        """ Get the logger name """
        res = type(self).__name__

        if self._id:
            res += f".{self._id}"

        return res

    def _get_function_name(self) -> str:
        """
        Get function name of calling method

        :return: The name of the calling function
            (expected to be called in self.error/debug/..)
        """
        fname = inspect.getframeinfo(inspect.stack()[2][0]).function

        if fname == "<module>":
            return ""
        else:
            return fname

    def log(self, level: int, msg: Any, *args, **kwargs) -> None:
        """ Log a message given log level with internal logger """
        # TODO: _get_function_name not required - python supports this out-of-the-box
        self._logger.log(
            level, msg,
            extra={'function': self._get_function_name()},
            *args, **kwargs
        )

    def exception(self, msg: Any, *args, **kwargs) -> None:
        """ Exception 'msg' with internal logger """
        self._logger.exception(
            msg,
            extra={'function': self._get_function_name()},
            *args, **kwargs
        )

    def debug(self, msg: Any, *args, **kwargs) -> None:
        """ Debug 'msg' with internal logger """
        self._logger.debug(
            msg,
            extra={'function': self._get_function_name()},
            *args, **kwargs
        )

    def info(self, msg: Any, *args, **kwargs) -> None:
        """ Info 'msg' with internal logger """
        self._logger.info(
            msg,
            extra={'function': self._get_function_name()},
            *args, **kwargs
        )

    def warning(self, msg: Any, *args, **kwargs) -> None:
        """ Warning 'msg' with internal logger """
        self._logger.warning(
            msg,
            extra={'function': self._get_function_name()},
            *args, **kwargs
        )

    def error(self, msg: Any, *args, **kwargs) -> None:
        """ Error 'msg' with internal logger """
        self._logger.error(
            msg,
            extra={'function': self._get_function_name()},
            *args, **kwargs
        )

    def critical(self, msg: Any, *args, **kwargs) -> None:
        """ Critical 'msg' with internal logger """
        self._logger.critical(
            msg,
            extra={'function': self._get_function_name()},
            *args, **kwargs
        )

    def fatal(self, msg: Any, *args, **kwargs) -> None:
        """ Fatal 'msg' with internal logger """
        self._logger.fatal(
            msg,
            extra={'function': self._get_function_name()},
            *args, **kwargs
        )


class ModuleLogable(Logable):
    """ Class to log on module level """

    def __init__(self, settings: Optional[Dict[str, Any]] = None) -> None:
        """ Constructor

        :param settings: Optional settings to apply
        """
        if settings is None:
            settings = {}

        super().__init__(settings)

    @property
    def name(self):
        """ Name of logger """
        return self.__module__


class LoggerLike(Protocol):
    """ Protocol looks like one of the loggers """

    def exception(self, msg: Any, *args, **kwargs) -> None:  # noqa D102
        ...

    def debug(self, msg: Any, *args, **kwargs) -> None:  # noqa D102
        ...

    def info(self, msg: Any, *args, **kwargs) -> None:  # noqa D102
        ...

    def warning(self, msg: Any, *args, **kwargs) -> None:  # noqa D102
        ...

    def error(self, msg: Any, *args, **kwargs) -> None:  # noqa D102
        ...

    def critical(self, msg: Any, *args, **kwargs) -> None:  # noqa D102
        ...

    def fatal(self, msg: Any, *args, **kwargs) -> None:  # noqa D102
        ...


def get_logger() -> LoggerLike:
    """ Get a logger instance for current file/module """
    frm = inspect.stack()[1]
    mod = inspect.getmodule(frm[0])

    if mod is None:
        logging.error(dir(frm))
        logging.error(dir(inspect.stack()[0]))

    class TempLogable(Logable):
        """ Class to log on module level """

        @property
        def name(self) -> str:
            if mod is None:
                return ""

            return mod.__name__

    logger = TempLogable()

    return logger


default_logging_config: Dict[str, Any] = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "threaded": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d "
                      "%(thread)d %(message)s"
        },
        "verbose": {
            "format": "%(asctime)s %(levelname)-8s [%(name)s%(function)s] "
                      "%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
        "colored": {
            "()": "colorlog.ColoredFormatter",
            "format":
                "%(blue,bold)s%(asctime)s%(reset)s "
                "%(log_color)s%(levelname)-8s%(reset)s"
                "%(blue)s[%(name)s%(function)s]%(reset)s "
                  "%(message_log_color)s%(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "log_colors": {
                "DEBUG": "cyan",
                "INFO": "green",
                "WARNING": "white,bg_yellow",
                "ERROR": "yellow,bg_red",
                "CRITICAL": "yellow,bg_red"
            },
            "secondary_log_colors": {
                "message": {
                    "DEBUG": "cyan",
                    "INFO": "green",
                    "WARNING": "yellow",
                    "ERROR": "red",
                    "CRITICAL": "red,bg_white"
                }
            }
        },
        "simple": {
            "format": "%(levelname)s %(message)s"
        }
    },
    "filters": {
        "my": {
            "()": "flotils.logable.FunctionFilter"
        }
    },
    "handlers": {
        "null": {
            "level": "DEBUG",
            "class": "logging.NullHandler",
            "filters": ["my"]
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "colored",
            "filters": ["my"]
        }
    },
    "loggers": {
        "": {
            "handlers": [
                "console"
            ],
            "propagate": True,
            "level": "INFO"
        }
    }
}

# Try to use colorlog as default -> if not installed, fallback solution
if colorlog is None:
    del default_logging_config['formatters']['colored']
    default_logging_config['handlers']['console']['formatter'] = "verbose"
