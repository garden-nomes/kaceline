from app import app
from app import mysql


@app.route('/')
@app.route('/index')
def index():
    cur = mysql.connection.cursor()
    cur.execute('select * from HD_TICKET')
    result = cur.fetchall()
    return str(result)
