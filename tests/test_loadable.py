# -*- coding: UTF-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

__author__ = "d01"
__email__ = "jungflor@gmail.com"
__copyright__ = "Copyright (C) 2019, Florian JUNG"
__license__ = "MIT"
__version__ = "0.1.0"
__date__ = "2019-03-26"
# Created: 2019-03-21 16:02

import datetime

import flotils


logger = flotils.get_logger()


def test_save_load_json():
    now = datetime.datetime.utcnow()
    delta = datetime.timedelta(
        days=1, hours=1, seconds=1
    )
    data = {
        'datetime': now,
        'date': now.date(),
        'delta': delta,
        'time': now.time(),
    }
    flotils.save_file("tmp/file.json", data, readable=True)
    loaded = flotils.load_file("tmp/file.json")
    assert now == loaded['datetime']
    assert now.date() == loaded['date']
    assert delta == loaded['delta']
    assert now.time() == loaded['time']


if __name__ == "__main__":
    import logging.config
    from flotils.logable import default_logging_config

    logging.config.dictConfig(default_logging_config)
    logging.getLogger().setLevel(logging.DEBUG)

    test_save_load_json()
