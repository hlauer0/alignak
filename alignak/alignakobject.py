# -*- coding: utf-8 -*-

#
# Copyright (C) 2015-2015: Alignak team, see AUTHORS.txt file for contributors
#
# This file is part of Alignak.
#
# Alignak is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Alignak is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Alignak.  If not, see <http://www.gnu.org/licenses/>.
#
""" This module contains only a common class for all object created in Alignak: AlignakObject.
"""

import uuid
from alignak.property import SetProp, StringProp


class AlignakObject(object):
    """This class provide a generic way to instantiate alignak objects.
    Attribute are ser dynamically, whether we un-serialize them create them at run / parsing time

    """

    properties = {'uuid': StringProp(default='')}
    macros = {}

    def __init__(self, params=None, parsing=True):  # pylint: disable=W0613

        if params is None:
            return
        all_props = {}
        all_props.update(getattr(self, "properties", {}))
        all_props.update(getattr(self, "running_properties", {}))
        for key, value in params.iteritems():
            if key in all_props and isinstance(all_props[key], SetProp):
                setattr(self, key, set(value))
            else:
                setattr(self, key, value)

        if not hasattr(self, 'uuid'):
            self.uuid = uuid.uuid4().hex

    def serialize(self):
        """This function serialize into a simple dict object.
        It is used when transferring data to other daemons over the network (http)

        Here is the generic function that simply export attributes declared in the
        properties dictionary of the object.

        :return: Dictionary containing key and value from properties
        :rtype: dict
        """
        cls = self.__class__
        # id is not in *_properties
        res = {'uuid': self.uuid}
        for prop in cls.properties:
            if hasattr(self, prop):
                if isinstance(cls.properties[prop], SetProp):
                    res[prop] = list(getattr(self, prop))
                else:
                    res[prop] = getattr(self, prop)

        return res

    def fill_default(self):
        """
        Define properties with default value when not defined

        :return: None
        """
        cls = self.__class__

        for prop, entry in cls.properties.items():
            if not hasattr(self, prop) and entry.has_default:
                setattr(self, prop, entry.default)
