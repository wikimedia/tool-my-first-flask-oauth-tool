My first Flask OAuth tool
=========================

This git repository contains the source code for a basic Python webservice
built using the Flask framework. It shows how to use the `mwoath` library to
manage OAuth authentication with a MediaWiki server.

Deploy on Toolforge
-------------------
See https://wikitech.wikimedia.org/wiki/Help:Toolforge/My_first_Flask_OAuth_tool
for a detailed tutorial describing the full process of creating a tool account
and running this tool.

```
$ ssh login.toolforge.org
$ become $TOOL_NAME
$ cat > $HOME/service.template << EOF
backend: kubernetes
type: python3.7
canonical: true
EOF
$ mkdir -p $HOME/www/python
$ git clone https://phabricator.wikimedia.org/source/tool-my-first-flask-oauth-tool.git \
  $HOME/www/python/src
$ touch $HOME/www/python/src/config.yaml
$ chmod u=rw,go= $HOME/www/python/src/config.yaml
$ cat > $HOME/www/python/src/config.yaml << EOF
SESSION_COOKIE_PATH: /$TOOL_NAME
SECRET_KEY: $(python -c "import os; print repr(os.urandom(24))")
CONSUMER_KEY: $KEY_YOU_GOT_FROM_OAUTH_REGISTRATION
CONSUMER_SECRET: $SECRET_YOU_GOT_FROM_OAUTH_REGISTRATION
EOF
$ webservice shell
$ python3 -m venv $HOME/www/python/venv
$ source $HOME/www/python/venv/bin/activate
$ pip install --upgrade pip
$ pip install -r $HOME/www/python/src/requirements.txt
$ exit
$ webservice start
```

License
-------
[GNU GPLv3+](//www.gnu.org/copyleft/gpl.html "GNU GPLv3+")
