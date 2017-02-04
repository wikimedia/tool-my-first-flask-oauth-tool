# -*- coding: utf-8 -*-
#
# This file is part of the Tool Labs Flask + OAuth WSGI tutorial
#
# Copyright (C) 2017 Bryan Davis and contributors
#
# This program is free software: you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
# more details.
#
# You should have received a copy of the GNU General Public License along
# with this program.  If not, see <http://www.gnu.org/licenses/>.

import flask
import os
import yaml

app = flask.Flask(__name__)

__dir__ = os.path.dirname(__file__)
app.config.update(
    yaml.load(open(os.path.join(__dir__, 'default_config.yaml'))))
try:
    app.config.update(
        yaml.load(open(os.path.join(__dir__, 'config.yaml'))))
except IOError:
    # It is ok if there is no local config file
    pass


@app.route('/')
def index():
  return app.config['GREETING']
