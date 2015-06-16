from MySQLdb.cursors import DictCursor
from flask import render_template
from app import app
from app import mysql


@app.route('/')
@app.route('/index')
def index():
    """ home page view, basically all of the stuff will go here.
    """
    cur = mysql.connection.cursor(cursorclass=DictCursor)
    cur.execute(
        'select * from HD_TICKET'
        'where MODIFIED < NOW() - INTERVAL 1 WEEK'
        'and HD_QUEUE_ID = 18')
    results = [ticket for ticket in cur.fetchall()]
    results.sort(key=lambda t: t['MODIFIED'])
    return render_template('timeline.html',
                           title='kaceline',
                           tickets=results)


@app.route('/changes')
def changes():
    return NotImplementedError
