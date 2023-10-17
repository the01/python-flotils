# -*- coding: UTF-8 -*-

__author__ = "d01"
__email__ = "jungflor@gmail.com"
__copyright__ = "Copyright (C) 2018-23, Florian JUNG"
__license__ = "MIT"
__version__ = "0.1.0"
__date__ = "2023-10-17"
# Created: 2018-01-27 10:44

import abc
from typing import Any, Dict, Optional

from typing_extensions import Self


def format_vars(instance: Any) -> str:
    """
    Get key, val as string for all properties

    :param instance: Instance to iterate over
    :returns: Formatted string list of properties
    """
    attrs = vars(instance)

    return ", ".join(
        f"{key}={value}"
        for key, value in attrs.items()
    )


class FromToDictBase(abc.ABC):  # noqa B024
    """ Class allowing automatic loading to and from dicts of attributes """

    @classmethod
    def from_dict(cls, d: Optional[Dict[str, Any]]) -> Self:
        """
        Instantiate from dict

        :param d: Dict to load from
        :returns: Instance with values set
        """
        new = cls()

        if not d:
            return new

        attrs = vars(new)

        for key in d:
            if key in attrs:
                # both in dict and this class
                setattr(new, key, d[key])

        return new

    def to_dict(self) -> Dict[str, Any]:
        """
        Transform object to dict

        :returns: Dict representing current instance
        """
        attrs = vars(self)
        res = {}

        for key, value in attrs.items():
            if isinstance(value, FromToDictBase):
                res[key] = value.to_dict()
            else:
                res[key] = value

        return res

    def clone(self) -> Self:
        """
        Create new instance from current

        Saves to dict and reloads it. Not all values may be new instances

        :returns: New instance with current values
        """
        return self.from_dict(self.to_dict())


class PrintableBase(abc.ABC):  # noqa B024
    """ Class with auto readable values """

    def __str__(self) -> str:
        """ View for user """
        return "<{}>({})".format(
            self.__class__.__name__, format_vars(self)
        )

    def __repr__(self) -> str:
        """ View for programmer """
        return self.__str__()
