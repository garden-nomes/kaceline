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
        ' where MODIFIED > NOW() - INTERVAL 1 WEEK'
        ' and HD_QUEUE_ID = 18')
    tickets = [ticket for ticket in cur.fetchall()]
    tickets.sort(key=lambda t: t['MODIFIED'])
    changes = []
    for ticket in tickets:
        cur.execute(
            'select * from HD_TICKET_CHANGE'
            ' where HD_TICKET_ID = %s' % (ticket['ID']))
        changes.append([change for change in cur.fetchall()])

    # put all the data into one place for passing into template
    # list of ticket changes as dicts
    data = [[{'ticket_id': change['HD_TICKET_ID'],
              'submitter_id': change['USER_ID'],
              'description': change['DESCRIPTION'],
              'ticket_title': [t['TITLE'] for t in tickets
                               if t['ID'] == change['HD_TICKET_ID']][0]}
             for change in c] for c in changes]
    print data
    return render_template('timeline.html',
                           title='kaceline',
                           data=data)


@app.route('/changes')
def changes():
    return NotImplementedError
