# (C) Copyright 2020 ECMWF.
#
# This software is licensed under the terms of the Apache Licence Version 2.0
# which can be obtained at http://www.apache.org/licenses/LICENSE-2.0.
# In applying this licence, ECMWF does not waive the privileges and immunities
# granted to it by virtue of its status as an intergovernmental organisation nor
# does it submit to any jurisdiction.
#

import os


CACHE = {}


def _find_plugin(directory, name):
    n = len(directory)
    for path, dirs, files in os.walk(directory):
        path = path[n:]
        for f in files:
            if f.endswith(".yaml"):
                if f[:-5] == name:
                    return False, os.path.join(directory, path, f)

            if f.endswith(".py"):
                p = os.path.join(path, f[:-3])
                if p[0] != "/":
                    p = "/" + p
                if p[1:].replace("/", "-").replace("_", "-") == name:
                    return True, p.replace("/", ".")

    raise Exception("Cannot find plugin '%s' in %s" % (name, directory))


def find_plugin(directory, name, module_callback, yaml_callcack):
    if (directory, name) not in CACHE:
        CACHE[(directory, name)] = _find_plugin(directory, name)

    code, plugin = CACHE[(directory, name)]
    if code:
        return module_callback(plugin)
    else:
        return yaml_callcack(plugin)
