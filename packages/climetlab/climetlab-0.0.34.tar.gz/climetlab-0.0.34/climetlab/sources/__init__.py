# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.
#

from importlib import import_module
import os


def lookup(name):
    source = import_module(".%s" % (name.replace("-", "_"),), package=__name__)
    return source.source


def load(name, *args, **kwargs):
    return lookup(name)(*args, **kwargs)


def list_entries():
    here = os.path.realpath(os.path.dirname(__file__))
    result = []

    for n in os.listdir(here):
        if n.startswith("."):
            continue

        if n.startswith("_"):
            continue

        if not n.endswith(".py"):
            continue

        result.append(n[:-3])

    return result


class DataSource:
    def __init__(self, **kwargs):
        self._kwargs = kwargs

    sphinxdoc = """
        No help
    """

    # def __iter__(self):
    #     raise NotImplementedError("%r: method __iter__() not implemented" % (self.__class__.__name__,))

    # def __len__(self):
    #     raise NotImplementedError("%r: method __len__() not implemented" % (self.__class__.__name__,))

    # def __getitem__(self, n):
    #     raise NotImplementedError("%r: method __getitem__() not implemented" % (self.__class__.__name__,))

    # def to_xarray(self, *args, **kwargs):
    #     raise NotImplementedError("%r: method to_xarray() not implemented" % (self.__class__.__name__,))

    # def to_pandas(self, *args, **kwargs):
    #     raise NotImplementedError("%r: method to_pandas() not implemented" % (self.__class__.__name__,))

    # def to_numpy(self, *args, **kwargs):
    #     raise NotImplementedError("%r: method to_numpy() not implemented" % (self.__class__.__name__,))

    # def to_metview(self, *args, **kwargs):
    #     raise NotImplementedError("%r: method to_metview() not implemented" % (self.__class__.__name__,))
