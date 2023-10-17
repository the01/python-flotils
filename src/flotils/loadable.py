# -*- coding: UTF-8 -*-
""" Module for loading/saving data/classes with json """

__author__ = "the01"
__email__ = "jungflor@gmail.com"
__copyright__ = "Copyright (C) 2013-23, Florian JUNG"
__license__ = "MIT"
__version__ = "0.5.0"
__date__ = "2023-10-17"
# Created: 2014-08-29 09:38

import datetime
import io
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, TextIO, Type, Union
from warnings import warn

import yaml

from .logable import Logable


MSG_DEPRECATED = "Serializing with '{}' keys is deprecated. Use '__type__' instead"
TYPE_ALL = Union[None, str, int, float, bool, Dict, List]
TYPE_DATETIME = Union[
    datetime.datetime, datetime.date, datetime.time, datetime.timedelta,
]


# TODO: New format according to https://gist.github.com/majgis/4200488
class DateTimeEncoder(json.JSONEncoder):
    """ Encode datetime, date and time objects for json """

    def default(self, obj: Any) -> Union[Dict[str, Any], Any]:
        """ Serialize object """
        if isinstance(obj, datetime.datetime):
            # Save all without tz info as UTC
            if obj.tzinfo:
                offset = obj.tzinfo.utcoffset(obj)

                if offset:
                    obj = obj - offset

                obj = obj.replace(tzinfo=None)

            return {
                '__type__': "datetime",
                '__value__': obj.isoformat() + "Z"
            }
        elif isinstance(obj, datetime.date):
            return {
                '__type__': "date",
                '__value__': obj.isoformat()
            }
        elif isinstance(obj, datetime.timedelta):
            # Time delta only stores days, seconds and microseconds
            return {
                '__type__': "timedelta",
                'days': obj.days,
                'seconds': obj.seconds,
                'microseconds': obj.microseconds,
            }
        elif isinstance(obj, datetime.time):
            return {
                '__type__': "time",
                '__value__': obj.isoformat()
            }

        return super(DateTimeEncoder, self).default(obj)


# TODO: Load datetime as utc but without tzinfo set
class DateTimeDecoder(object):
    """ Decode datetime, date and time from json """

    @staticmethod
    def _as_datetime(dct: Dict[str, Any]) -> datetime.datetime:
        """
        Try to load dict as datetime

        :param dct: Dict with potential serialized datetime
        :returns: Loaded datetime
        :raises TypeError: Not a datetime
        :raises KeyError: No '__value__' field
        :raises Exception: Failed to parse datetime
        """
        if "__datetime__" in dct.keys():
            warn(
                MSG_DEPRECATED.format("__datetime__"),
                DeprecationWarning, stacklevel=2
            )
            dct = {
                '__type__': "datetime",
                '__value__': dct['__datetime__'],
            }

        if dct.get('__type__', None) == "datetime":
            # Should be UTC
            try:
                return datetime.datetime.strptime(
                    dct['__value__'], "%Y-%m-%dT%H:%M:%S.%fZ"
                )
            except ValueError:
                return datetime.datetime.strptime(
                    dct['__value__'], "%Y-%m-%dT%H:%M:%SZ"
                )

        raise TypeError("Not Datetime")

    @staticmethod
    def _as_date(dct: Dict[str, Any]) -> datetime.date:
        """
        Try to load dict as date

        :param dct: Dict with potential serialized date
        :returns: Loaded date
        :raises TypeError: Not a date
        :raises KeyError: No '__value__' field
        :raises Exception: Failed to parse date
        """
        if "__date__" in dct:
            warn(
                MSG_DEPRECATED.format("__date__"),
                DeprecationWarning, stacklevel=2
            )
            dct = {
                '__type__': "date",
                '__value__': dct['__date__'],
            }

        if dct.get('__type__', None) == "date":
            d = datetime.datetime.strptime(
                dct['__value__'], "%Y-%m-%d"
            )

            if d:
                return d.date()

        raise TypeError("Not Date")

    @staticmethod
    def _as_time(dct: Dict[str, Any]) -> datetime.time:
        """
        Try to load dict as time

        :param dct: Dict with potential serialized time
        :returns: Loaded time
        :raises TypeError: Not a time
        :raises KeyError: No '__value__' field
        :raises Exception: Failed to parse time
        """
        if "__time__" in dct:
            warn(
                MSG_DEPRECATED.format("__time__"),
                DeprecationWarning, stacklevel=2
            )
            dct = {
                '__type__': "time",
                '__value__': dct['__time__'],
            }

        if dct.get('__type__', None) == "time":
            try:
                d = datetime.datetime.strptime(
                    dct['__value__'], "%H:%M:%S.%f"
                )
            except ValueError:
                d = datetime.datetime.strptime(
                    dct['__value__'], "%H:%M:%S"
                )

            if d:
                return d.time()

        raise TypeError("Not Time")

    @staticmethod
    def decode(
            dct: Union[Any, Dict[str, Any]]
    ) -> Union[TYPE_ALL, TYPE_DATETIME]:
        """ Decode json data into actual objects """
        if not isinstance(dct, dict):
            return dct

        if "__type__" in dct:
            obj_type = dct.pop('__type__')

            if obj_type == "timedelta":
                return datetime.timedelta(**dct)

            # Not matched
            dct['__type__'] = obj_type

        try:
            return DateTimeDecoder._as_datetime(dct)
        except Exception:  # nosec B110
            pass
        try:
            return DateTimeDecoder._as_date(dct)
        except Exception:  # nosec B110
            pass
        try:
            return DateTimeDecoder._as_time(dct)
        except Exception:  # nosec B110
            pass

        return dct


# Return Type depends on the decoder
def load_json(
        json_data: str, decoder: Optional[Type[DateTimeDecoder]] = None
) -> Any:
    """
    Load data from json string

    :param json_data: Stringified json object
    :param decoder: Use custom json decoder
    :type decoder: T <= DateTimeDecoder
    :return: Json data
    """
    if decoder is None:
        decoder = DateTimeDecoder

    return json.loads(json_data, object_hook=decoder.decode)


def load_json_file(
        file: Union[TextIO, str, Path], decoder: Optional[Type[DateTimeDecoder]] = None
) -> Any:
    """
    Load data from json file

    :param file: Readable object or path to file
    :param decoder: Use custom json decoder
    :type decoder: T <= DateTimeDecoder
    :return: Json data
    """
    if decoder is None:
        decoder = DateTimeDecoder

    if not hasattr(file, "read"):
        with io.open(file, "r", encoding="utf-8") as f:
            return json.load(f, object_hook=decoder.decode)

    return json.load(file, object_hook=decoder.decode)


# Type of val depends on encoder
def save_json(
        val: Any,
        pretty: bool = False, sort: bool = True,
        encoder: Optional[Type[DateTimeEncoder]] = None
) -> str:
    """
    Save data to json string

    :param val: Value or struct to save
    :type val: None | int | float | str | list | dict
    :param pretty: Format data to be readable (default: False)
                    otherwise going to be compact
    :param sort: Sort keys (default: True)
    :param encoder: Use custom json encoder
    :type encoder: T <= DateTimeEncoder
    :return: The jsonified string
    """
    if encoder is None:
        encoder = DateTimeEncoder

    if pretty:
        data = json.dumps(
            val,
            indent=4,
            separators=(',', ': '),
            sort_keys=sort,
            cls=encoder
        )
    else:
        data = json.dumps(
            val,
            separators=(',', ':'),
            sort_keys=sort,
            cls=encoder
        )

    return data


def save_json_file(
        file: Union[TextIO, str, Path], val: Any,
        pretty: bool = False, compact: bool = True, sort: bool = True,
        encoder: Optional[Type[DateTimeEncoder]] = None
) -> None:
    """
    Save data to json file

    :param file: Writable object or path to file
    :param val: Value or struct to save
    :param pretty: Format data to be readable (default: False)
    :param compact: Format data to be compact (default: True)
    :param sort: Sort keys (default: True)
    :param encoder: Use custom json encoder
    :type encoder: T <= DateTimeEncoder
    """
    # TODO: make pretty/compact into one bool?
    if encoder is None:
        encoder = DateTimeEncoder

    opened = False

    if not hasattr(file, "write"):
        file = io.open(file, "w", encoding="utf-8")
        opened = True

    try:
        if pretty:
            data = json.dumps(
                val,
                indent=4,
                separators=(',', ': '),
                sort_keys=sort,
                cls=encoder
            )
        elif compact:
            data = json.dumps(
                val,
                separators=(',', ':'),
                sort_keys=sort,
                cls=encoder
            )
        else:
            data = json.dumps(val, sort_keys=sort, cls=encoder)

        file.write(data)
    finally:
        if opened:
            # For type hinting
            assert isinstance(file, TextIO)  # nosec B101

            file.close()


def load_yaml(data: str) -> TYPE_ALL:
    """
    Load data from yaml string

    :param data: Stringified yaml object
    :return: Yaml data
    """
    return yaml.safe_load(data)


def load_yaml_file(file: Union[TextIO, str, Path]) -> TYPE_ALL:
    """
    Load data from yaml file

    :param file: Readable object or path to file
    :return: Yaml data
    """
    if not hasattr(file, "read"):
        with io.open(file, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    return yaml.safe_load(file)


def save_yaml(val: TYPE_ALL) -> str:
    """
    Save data to yaml string

    :param val: Value or struct to save
    :return: The yamlified string
    """
    return yaml.safe_dump(val)


def save_yaml_file(file: Union[TextIO, str, Path], val: TYPE_ALL) -> None:
    """
    Save data to yaml file

    :param file: Writable object or path to file
    :param val: Value or struct to save
    """
    opened = False

    if not hasattr(file, "write"):
        file = io.open(file, "w", encoding="utf-8")
        opened = True

    try:
        yaml.safe_dump(val, file)
    finally:
        if opened:
            # For type hinting
            assert isinstance(file, TextIO)  # nosec B101

            file.close()


def load_file(path: Union[str, Path]) -> Union[TYPE_ALL, TYPE_DATETIME]:
    """
    Load file

    :param path: Path to file
    :return: Loaded data
    :raises IOError: If file not found or error accessing file
    """
    res: Union[TYPE_ALL, TYPE_DATETIME] = None

    if not path:
        IOError("No path specified to save")

    p = Path(path)

    if not p.is_file():
        raise IOError("File not found {}".format(path))

    try:
        with p.open("r", encoding="utf-8") as f:
            if p.suffix.lower() == ".json":
                res = load_json_file(f)
            elif p.suffix.lower() == ".yaml" or p.suffix.lower() == ".yml":
                res = load_yaml_file(f)
    except IOError:
        raise
    except Exception as e:
        raise IOError(e)

    return res


def save_file(path: Union[str, Path], data: TYPE_ALL, readable: bool = False) -> None:
    """
    Save to file

    :param path: File path to save
    :param data: Data to save
    :param readable: Format file to be human readable (default: False)
    :raises IOError: If empty path or error writing file
    """
    if not path:
        IOError("No path specified to save")

    p = Path(path)

    try:
        with p.open("w", encoding="utf-8") as f:
            if p.suffix.lower() == ".json":
                save_json_file(
                    f,
                    data,
                    pretty=readable,
                    compact=(not readable),
                    sort=True
                )
            elif p.suffix.lower() == ".yaml" or p.suffix.lower() == ".yml":
                save_yaml_file(f, data)
    except IOError:
        raise
    except Exception as e:
        raise IOError(e)


def join_path_prefix(
        path: Union[str, Path], pre_path: Optional[Union[str, Path]] = None
) -> Optional[Path]:
    """
    If path set and not absolute, append it to pre path (if used)

    :param path: path to append
    :param pre_path: Base path to append to (default: None)
    :return: Path or appended path
    """
    if path is None:
        return path

    p = Path(path)

    if pre_path is not None and not p.is_absolute():
        return Path(pre_path) / p

    return p


class Loadable(Logable):
    """ Class to facilitate loading config from json-files and ease relative paths """

    def __init__(self, settings: Optional[Dict[str, Any]] = None):
        """
        Initialize object

        :param settings: Settings for instance (default: None)
        :raises IOError: Failed to load settings file
        """
        if settings is None:
            settings = {}

        super().__init__(settings)

        sett_path = settings.get('settings_file', None)
        self._pre_path = settings.get('path_prefix', None)

        if sett_path:
            sett_path = self.join_path_prefix(sett_path)
            sett = self.load_settings(sett_path)
            sett_prepath = sett.get('path_prefix')

            if sett_prepath:
                # if sett_path is absolute path
                # -> set to sett_path else join with dict path_prefix
                self._pre_path = self.join_path_prefix(sett_prepath)

            # settings in constructor overwrite settings from file
            sett.update(settings)
            settings.update(sett)
            self.debug(f"Loaded config {sett_path}")
            # to apply loaded settings to logable as well
            super(Loadable, self).__init__(settings)

    def join_path_prefix(self, path: Optional[Union[str, Path]]) -> Optional[Path]:
        """
        If path set and not absolute, append it to self._pre_path

        :param path: Path to append
        :return: Path or appended path
        """
        if path is None:
            return None

        return join_path_prefix(path, self._pre_path)

    def _load_json_file(
            self,
            file: Union[TextIO, str, Path],
            decoder: Optional[Type[DateTimeDecoder]] = None,
    ) -> Any:
        """
        Load data from json file

        :param file: Readable file or path to file
        :param decoder: Use custom json decoder
        :type decoder: T <= flotils.loadable.DateTimeDecoder
        :return: Json data
        :raises IOError: Failed to load
        """
        try:
            res = load_json_file(file, decoder=decoder)
        except ValueError as e:
            if f"{e}" == "No JSON object could be decoded":
                raise IOError("Decoding JSON failed")

            self.exception(f"Failed to load from {file}")

            raise IOError("Loading file failed")
        except Exception:
            self.exception(f"Failed to load from {file}")

            raise IOError("Loading file failed")

        return res

    def _save_json_file(
        self,
            file: Union[TextIO, str, Path], val: Any,
            pretty: bool = False, compact: bool = True, sort: bool = True,
            encoder: Optional[Type[DateTimeEncoder]] = None
    ) -> None:
        """
        Save data to json file

        :param file: Writable object or path to file
        :param val: Value or struct to save
        :param pretty: Format data to be readable (default: False)
        :param compact: Format data to be compact (default: True)
        :param sort: Sort keys (default: True)
        :param encoder: Use custom json encoder
        :type encoder: T <= DateTimeEncoder
        :raises IOError: Failed to save
        """
        try:
            save_json_file(file, val, pretty, compact, sort, encoder)
        except Exception:
            self.exception(f"Failed to save to {file}")

            raise IOError("Saving file failed")

    def _load_yaml_file(self, file: Union[TextIO, str, Path]) -> TYPE_ALL:
        """
        Load data from yaml file

        :param file: Readable object or path to file
        :return: Yaml data
        :raises IOError: Failed to load
        """
        try:
            res = load_yaml_file(file)
        except Exception:
            self.exception(f"Failed to load from {file}")

            raise IOError("Loading file failed")

        return res

    def _save_yaml_file(self, file: Union[TextIO, str, Path], val: TYPE_ALL) -> None:
        """
        Save data to yaml file

        :param file: Writable object or path to file
        :param val: Value or struct to save
        :raises IOError: Failed to save
        """
        try:
            save_yaml_file(file, val)
        except Exception:
            self.exception(f"Failed to save to {file}")

            raise IOError("Saving file failed")

    def load_settings(self, path: Union[str, Path]) -> Dict[str, Any]:
        """
        Load settings dict

        :param path: Path to settings file
        :return: Loaded settings
        :raises IOError: If file not found or error accessing file
        :raises TypeError: Settings file does not contain dict
        """
        res = self.load_file(path)

        if not isinstance(res, dict):
            raise TypeError("Expected settings to be dict")

        return res

    def save_settings(
            self, path: Union[str, Path],
            settings: Dict[str, Any],
            readable: bool = False
    ) -> None:
        """
        Save settings to file

        :param path: File path to save
        :param settings: Settings to save
        :param readable: Format file to be human-readable (default: False)
        :raises IOError: If empty path or error writing file
        :raises TypeError: Settings is not a dict
        """
        if not isinstance(settings, dict):
            raise TypeError("Expected settings to be dict")

        return self.save_file(path, settings, readable)

    def load_file(self, path: Union[str, Path]) -> Union[TYPE_ALL, TYPE_DATETIME]:
        """
        Load file

        :param path: Path to file
        :return: Loaded settings
        :raises IOError: If file not found or error accessing file
        """
        res = None

        if not path:
            IOError("No path specified to save")

        p = Path(path)

        if not p.is_file():
            raise IOError(f"File not found {p}")

        try:
            with p.open("r", encoding="utf-8") as f:
                if p.suffix.lower() == ".json":
                    res = self._load_json_file(f)
                elif p.suffix.lower() == ".yaml" or p.suffix.lower() == ".yml":
                    res = self._load_yaml_file(f)
        except IOError:
            raise
        except Exception as e:
            self.exception(f"Failed reading {p}")

            raise IOError(e)

        return res

    def save_file(
            self, path: Union[str, Path],
            data: TYPE_ALL,
            readable: bool = False
    ) -> None:
        """
        Save to file

        :param path: File path to save
        :param data: To save
        :param readable: Format file to be human-readable (default: False)
        :raises IOError: If empty path or error writing file
        """
        if not path:
            IOError("No path specified to save")

        p = Path(path)

        try:
            with p.open("w", encoding="utf-8") as f:
                if p.suffix.lower() == ".json":
                    self._save_json_file(
                        f,
                        data,
                        pretty=readable,
                        compact=(not readable),
                        sort=True,
                    )
                elif p.suffix.lower() == ".yaml" or p.suffix.lower() == ".yml":
                    self._save_yaml_file(f, data)
        except IOError:
            raise
        except Exception as e:
            self.exception(f"Failed writing {p}")

            raise IOError(e)
