# -*- coding: UTF-8 -*-
""" Module for runable interfaces """

__author__ = "the01"
__email__ = "jungflor@gmail.com"
__copyright__ = "Copyright (C) 2015-23, Florian JUNG"
__license__ = "All rights reserved"
__version__ = "0.1.4"
__date__ = "2023-10-17"
# Created: 2015-06-07 15:00

from abc import ABC, abstractmethod
import signal
import time
from typing import Any, Dict, Optional
import warnings

from .logable import Logable


class StartError(Exception):
    """ Instance failed to start """


class StartException(StartError):  # noqa N818
    """ Deprecated - Use StartError """

    warnings.warn(
        "Deprecated - Use StartError",
        category=DeprecationWarning,
        stacklevel=2,
    )


class Startable(ABC):
    """ Abstract interface to add a start method """

    def __init__(self, settings: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize object

        :param settings: Settings to be passed for init (default: None)
        """
        if settings is None:
            settings = {}

        super().__init__()

    @abstractmethod
    def start(self) -> None:
        """ Start the interface """


class Stopable(ABC):
    """ Abstract interface to add a stop method """

    def __init__(self, settings: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize object

        :param settings: Settings to be passed for init (default: None)
        """
        if settings is None:
            settings = {}

        super().__init__()

    @abstractmethod
    def stop(self) -> None:
        """ Stop the interface """


class StartStopable(Startable, Stopable, ABC):
    """ Abstract interface to add a start/stop method (e.g. for threading) """

    def __init__(self, settings: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize object

        :param settings: Settings to be passed for init (default: None)
        """
        if settings is None:
            settings = {}

        super().__init__(settings)

        self._is_running: bool = False
        """ Indicate whether this object is currently running """
        self._start_block_timeout: float = settings.get('start_blocking_timeout', 1.0)
        """ Timeout used to sleep in blocking loop (in seconds) """

    @property
    def is_running(self) -> bool:
        """ Is this class currently running """
        return self._is_running

    def start(self, blocking: bool = False) -> None:
        """
        Start the interface

        :param blocking: Should the call block until stop() is called
            (default: False)
        :raises IOError: Only if it starts with "[errno 4]"
        :raises Exception: All exception
        """
        super().start()
        self._is_running = True

        # blocking
        try:
            while blocking and self._is_running:
                time.sleep(self._start_block_timeout)
        except IOError as e:
            if not str(e).lower().startswith("[errno 4]"):
                raise

    def stop(self) -> None:
        """ Stop the interface """
        self._is_running = False

        super().stop()


class SignalStopWrapper(Logable, Stopable, ABC):
    """ Catch SIGINT and SIGTERM to smoothly stop running """

    def __init__(self, settings: Optional[Dict[str, Any]] = None) -> None:
        """
        Constructor

        :param settings: Settings to be passed for init (default: None)
        """
        if settings is None:
            settings = {}

        super().__init__(settings)

        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        self.info("Catching SIGINT and SIGTERM")

    def _signal_handler(self, sig: int, frame: Any) -> None:
        """ Receive signals and stop instance """
        self.warning(f"Signal {sig} caught")
        self.stop()
