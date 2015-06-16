from MySQLdb.cursors import DictCursor
from flask import render_template
from app import app
from app import mysql


@app.route('/')
@app.route('/index')
def index():
    """ home page view, basically all of the stuff will go here.
    """
    # create cursor from database connection, which returns
    # entres as dictionary objects.
    cur = mysql.connection.cursor(cursorclass=DictCursor)
    # query for all the tickets from last week
    cur.execute('select * from HD_TICKET where MODIFIED < NOW() - INTERVAL 1 WEEK')
    results = [e for e in cur.fetchall() if ]
    # render the template and pass in most recent ticket changes
    return render_template('timeline.html',
                           title='kaceline')


@app.route('/changes')
def changes():
    return NotImplementedError
