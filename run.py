#!venv/bin/python
from werkzeug.contrib.fixers import ProxyFix
from app import app

app.wsgi_app = ProxyFix(app.wsgi_app)
app.run(debug=True)
