from MySQLdb.cursors import DictCursor
from collections import OrderedDict
from flask import render_template, request
from app import app
from app import mysql


def query_database(cur, time='WEEK'):  # helper function
    """ Input: cur -> MySQLdb cursor into database
               time -> a string containing one of ['DAY', 'WEEK', 'MONTH']
        Output: data -> All tickets and their associated changes from the
                        last day, week, or month.
    """
    cur.execute(  # build & execute query to grab relevant tickets
        'select * from HD_TICKET'
        ' where MODIFIED > NOW() - INTERVAL 1 %s'
        ' and HD_QUEUE_ID = 18' % time)  # interpolate desired time frame
    tickets = [ticket for ticket in cur.fetchall()]
    tickets.sort(key=lambda t: t['MODIFIED'])
    changes = []
    for ticket in tickets:
        cur.execute(  # for each ticket, grab associated changes
            'select * from HD_TICKET_CHANGE'
            ' where TIMESTAMP > NOW() - INTERVAL 1 %s'
            ' and HD_TICKET_ID = %s' % (time, ticket['ID']))
        changes.append([change for change in cur.fetchall()])

    cur.execute('select * from USER')
    users = [u for u in cur.fetchall()]
    # put all the data into one place for passing into template
    # as a list of lists of ticket change dictionaries
    data = [[{'ticket_id': change['HD_TICKET_ID'],
              'submitter_id':  change['USER_ID'],
              'submitter_name': [u['USER_NAME'] for u in users
                                 if u['ID'] == change['USER_ID']][0],
              'description': change['DESCRIPTION'],
              'timestamp': change['TIMESTAMP'],
              'comment': change['COMMENT'],
              'ticket_title': [t['TITLE'] for t in tickets
                               if t['ID'] == change['HD_TICKET_ID']][0]}
             for change in c] for c in changes]

    # join lists
    data = [change for sublist in data for change in sublist]

    # group by date
    new_data = OrderedDict()
    for change in sorted(data, key=lambda t: t['timestamp'], reverse=True):
        date = change['timestamp'].date()
        if date in new_data.keys():
            new_data[date].append(change)
        else:
            new_data[date] = [change]

    return new_data


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
def index(time=None):
    """ Home page view.
    """
    # create cursor into mysql database
    cur = mysql.connection.cursor(cursorclass=DictCursor)

    time = request.args.get('time')
    if time not in ['day', 'week', 'month']:
        time = 'week'

    data = query_database(cur, time)  # query db & render data
    return render_template('timeline.html',
                           title='kaceline',
                           data=data)


@app.route('/changes')
def changes():
    return NotImplementedError
