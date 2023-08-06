# -*- coding: utf-8 -*-
#
# Copyright (C) 2017-2019 KuraLabs S.R.L
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""
Class to load Flowbber Aggregator plugins.
"""

from functools import wraps
from collections import OrderedDict

from .loader import PluginLoader
from ..logging import get_logger
from ..components import Aggregator


log = get_logger(__name__)


class AggregatorsLoader(PluginLoader):
    """
    Aggregators plugins loader class.
    """

    _base_class = Aggregator
    _locally_registered = OrderedDict()

    def __init__(self):
        super().__init__('aggregators')


@wraps(AggregatorsLoader.register)
def register(key):
    return AggregatorsLoader.register(key)


__all__ = ['AggregatorsLoader', 'register']
