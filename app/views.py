from MySQLdb.cursors import DictCursor
from flask import render_template, request
from app import app
from app import mysql


def query_database(cur, time='WEEK'):  # helper function
    """ Input: cur -> MySQLdb cursor into database
               time -> a string containing one of ['DAY', 'WEEK', 'MONTH']
        Output: data -> All tickets and their associated changes from the
                        last day, week, or month.
    """
    cur.execute(
        'select * from HD_TICKET'
        ' where MODIFIED > NOW() - INTERVAL 1 %s'
        ' and HD_QUEUE_ID = 18' % time)
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
              'timestamp': change['TIMESTAMP'],
              'comment': change['COMMENT'],
              'ticket_title': [t['TITLE'] for t in tickets
                               if t['ID'] == change['HD_TICKET_ID']][0]}
             for change in c] for c in changes]

    return data


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index():
    """ home page view, basically all of the stuff will go here.
    """
    cur = mysql.connection.cursor(cursorclass=DictCursor)

    if request.method == 'POST':
        time = request.form['time']
        data = query_database(cur, time)
        return render_template('timeline.html',
                               title='kaceline',
                               data=data)

    else:
        data = query_database(cur)  # defaults to WEEK
        return render_template('timeline.html',
                               title='kaceline',
                               data=data)


@app.route('/changes')
def changes():
    return NotImplementedError
