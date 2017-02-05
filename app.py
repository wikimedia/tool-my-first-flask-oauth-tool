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
"""Example Flask application which can authenticate the user via OAuth."""

import flask
import mwoauth
import os
import werkzeug.contrib.fixers
import yaml


# Create the Flask application
app = flask.Flask(__name__)

# Add the ProxyFix middleware which reads X-Forwarded-* headers
app.wsgi_app = werkzeug.contrib.fixers.ProxyFix(app.wsgi_app)

# Load configuration from YAML file(s).
# See default_config.yaml for more information
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
    """Application landing page."""
    username = flask.session.get('username', None)
    return flask.render_template('index.html', username=username)


@app.route('/login')
def login():
    """Initiate an OAuth login.

    Call the MediaWiki server to get request secrets and then redirect the
    user to the MediaWiki server to sign the request.
    """
    consumer_token = mwoauth.ConsumerToken(
        app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])
    try:
        redirect, request_token = mwoauth.initiate(
            app.config['OAUTH_MWURI'], consumer_token)
    except Exception:
        app.logger.exception('mwoauth.initiate failed')
        flask.flash(u'OAuth handshake failed.' 'danger')
        flask.redirect(flask.url_for('index'))
    else:
        flask.session['request_token'] = dict(zip(
            request_token._fields, request_token))
        return flask.redirect(redirect)


@app.route('/oauth-callback')
def oauth_callback():
    """OAuth handshake callback.

    Validate the response from the MediaWiki server and call the MediaWiki API
    to get information about the user that has been authenticated.
    """
    if 'request_token' not in flask.session:
        flask.flash(u'OAuth callback failed. Are cookies disabled?', 'danger')
        return flask.redirect(flask.url_for('index'))

    consumer_token = mwoauth.ConsumerToken(
        app.config['CONSUMER_KEY'], app.config['CONSUMER_SECRET'])

    try:
        access_token = mwoauth.complete(
            app.config['OAUTH_MWURI'],
            consumer_token,
            mwoauth.RequestToken(**flask.session['request_token']),
            flask.request.query_string)

        identity = mwoauth.identify(
                app.config['OAUTH_MWURI'], consumer_token, access_token)

    except Exception:
        app.logger.exception('OAuth autnetication failed')
        flask.flask(u'OAuth authentication failed.')

    else:
        flask.session['access_token'] = dict(zip(
            access_token._fields, access_token))
        flask.session['username'] = identity['username']
        flask.flash(
            u'You were signed in, %s!' % identity['username'], 'success')

    return flask.redirect(flask.url_for('index'))


@app.route('/logout')
def logout():
    """Log the user out by clearing their session."""
    flask.session.clear()
    flask.flash(u'You have been logged out.', 'info')
    return flask.redirect(flask.url_for('index'))
