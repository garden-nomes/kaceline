from flask import Flask
from flask.ext.mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_USER'] = 'report'
app.config['MYSQL_PASSWORD'] = '***REMOVED***'
app.config['MYSQL_DB'] = 'ORG1'
app.config['MYSQL_PORT'] = 3306
mysql.init_app(app)

from app import views