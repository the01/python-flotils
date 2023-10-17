# -*- coding: UTF-8 -*-

""" An utility package """

__author__ = "the01"
__email__ = "jungflor@gmail.com"
__copyright__ = "Copyright (C) 2013-23, Florian JUNG"
__license__ = "MIT"
__date__ = "2023-10-17"

import logging

from .__version__ import __version__
from .convenience import FromToDictBase, PrintableBase
from .loadable import (
    load_file, load_json_file, load_yaml_file, Loadable,
    save_file, save_json_file, save_yaml_file,
)
from .logable import get_logger, Logable, ModuleLogable
from .runable import Startable, StartError, StartException, StartStopable, Stopable


logger = logging.getLogger(__name__)
__all__ = [
    "__version__",
    "logable", "Logable", "ModuleLogable", "get_logger",
    "loadable", "Loadable", "load_file", "save_file",
    "load_json_file", "save_json_file", "load_yaml_file", "save_yaml_file",
    "runable", "Startable", "StartError", "StartException", "Stopable", "StartStopable",
    "convenience", "FromToDictBase", "PrintableBase"
]
