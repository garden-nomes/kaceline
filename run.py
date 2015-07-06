#!flask/bin/python
# Startup development server with application.
from app import app
app.run(debug=True, host='0.0.0.0', port=80)
