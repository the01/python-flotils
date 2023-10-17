# -*- coding: UTF-8 -*-

import datetime
import logging
from pathlib import Path

from flotils.loadable import save_file, load_file, DateTimeEncoder, DateTimeDecoder


logger = logging.getLogger(__name__)


def test_save_load_json(tmp_path: Path):
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
    tmp_file = tmp_path / "file.json"
    save_file(tmp_file, data, readable=True)
    loaded = load_file(tmp_file)

    assert now == loaded['datetime']
    assert now.date() == loaded['date']
    assert delta == loaded['delta']
    assert now.time() == loaded['time']


def test_encode_datetime():
    now = datetime.datetime(2023, 10, 17, 1, 4, 36)

    result = DateTimeEncoder().encode(now)

    assert result == '{"__type__": "datetime", "__value__": "2023-10-17T01:04:36Z"}'


def test_encode_time():
    now = datetime.time(3, 55, 17, 1, )

    result = DateTimeEncoder().encode(now)

    assert result == '{"__type__": "time", "__value__": "03:55:17.000001"}'


def test_decode_datetime():
    result = DateTimeDecoder.decode({
        "__type__": "datetime", "__value__": "2023-10-17T01:04:36Z"
    })

    assert result == datetime.datetime(2023, 10, 17, 1, 4, 36)


def test_decode_datetime_deprecated():
    result = DateTimeDecoder.decode({
        "__datetime__": "2023-10-17T01:04:36Z"
    })

    assert result == datetime.datetime(2023, 10, 17, 1, 4, 36)
