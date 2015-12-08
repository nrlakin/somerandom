#!venv/bin/python
# Production startup script.
from app import app
app.run(debug=False)
