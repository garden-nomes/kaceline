from flask import Flask
from flask.ext.mysqldb import MySQL

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_USER'] = '*****'
app.config['MYSQL_HOST'] = 'kaceapp'
app.config['MYSQL_PASSWORD'] = '*****'
app.config['MYSQL_DB'] = 'ORG1'
app.config['MYSQL_PORT'] = 3306
mysql.init_app(app)

# import @ bottom to void circular references
from app import views
