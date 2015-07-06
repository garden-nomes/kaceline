from MySQLdb.cursors import DictCursor
from collections import OrderedDict
from datetime import date, timedelta, datetime
from flask import render_template, request
from app import app
from app import mysql


def query_database(cur, start, end, queue=18):  # helper function
    """ Input: cur -> MySQLdb cursor into database
               start, end -> datetime objects specifying an interval
                             (start <= end)
               queue -> an integer specifying the queue ID
        Output: data -> All tickets and their associated changes from the
                        last day, week, or month.
    """

    cur.execute(  # grab all ticket changes between certain time span
        'select HD_TICKET_CHANGE.HD_TICKET_ID,'
        ' HD_TICKET_CHANGE.USER_ID,'
        ' HD_TICKET_CHANGE.DESCRIPTION,'
        ' HD_TICKET_CHANGE.TIMESTAMP,'
        ' HD_TICKET_CHANGE.COMMENT,'
        ' HD_TICKET.TITLE,'
        ' HD_TICKET.ID,'
        ' HD_TICKET.HD_STATUS_ID, '
        ' USER.USER_NAME,'
        ' USER.ID'
        ' from HD_TICKET_CHANGE, HD_TICKET, USER'
        ' where HD_TICKET_CHANGE.TIMESTAMP between \'%s\' and \'%s\''
        ' and (select HD_TICKET.HD_QUEUE_ID from HD_TICKET'
        '   where HD_TICKET.ID = HD_TICKET_CHANGE.HD_TICKET_ID) = %s'
        ' and HD_TICKET.ID = HD_TICKET_CHANGE.HD_TICKET_ID'
        ' and USER.ID = HD_TICKET_CHANGE.USER_ID'
        % (start, end + timedelta(days=1), queue))
    data = cur.fetchall()

    for change in data:
        change['COMMENT'] = change['COMMENT'].splitlines()

    # group by date
    grouped_data = OrderedDict()
    for change in sorted(data, key=lambda t: t['TIMESTAMP'], reverse=True):
        date = change['TIMESTAMP'].date()
        if date in grouped_data.keys():
            grouped_data[date].append(change)
        else:
            grouped_data[date] = [change]

    return grouped_data


@app.route('/')
@app.route('/index', methods=['GET'])
def index():
    """ Home page view.
    """
    # create cursor into mysql database
    cur = mysql.connection.cursor(cursorclass=DictCursor)

    # process arguments
    start = request.args.get('start')
    end = request.args.get('end')
    queue = request.args.get('queue')

    if queue is None:
        queue = 18	# client management
    
    if start is None or end is None:
        end = date.today()
        start = end - timedelta(days=7)
    else:
        end = datetime.strptime(end, '%m/%d/%Y')
        start = datetime.strptime(start, '%m/%d/%Y')

    data = query_database(cur, start, end, queue)  # query db & render data
    return render_template('timeline.html',
                           title='kaceline',
                           data=data,
                           start=start,
                           end=end,
                           queue=queue)
