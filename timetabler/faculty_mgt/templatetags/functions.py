import datetime
from . import db_connect as db

def getYeah():
    now = datetime.datetime.now()
    return now.year


def pageData(icon, name):
    userdata = {
    'pageicon': icon,
    'pagetitle': name,
    'username': 'Sholanke Maxwell',
    'userimage': 'images/user.jpg',
    'copyrightyear': getYeah(),
    'notification_': 5,
    'messages_': 8,
    }
    return userdata

def getnewid(usedtype, menutype):
    query = ''
    if(usedtype == 'fac'):
        query = '''SELECT id FROM faculty_mgt_faculty ORDER BY id DESC LIMIT 1'''
    elif(usedtype == 'dpt'):
        query = '''SELECT id FROM faculty_mgt_faculty ORDER BY id DESC LIMIT 1'''
    elif(usedtype == 'lct'):
        query = '''SELECT id FROM faculty_mgt_faculty ORDER BY id DESC LIMIT 1'''

    db.cursor.execute(query)
    row = db.cursor.fetchone()
    count = row[0] + 1
    return usedtype.upper() + str(count)

def runInsertUpdateSql(name, code, table, query):
    # check if exist
    result = {
        'status': False,
        'message': '',
    }
    counter = int(db.cursor.execute('SELECT id FROM '+table+ ' WHERE code = \''+code+'\' LIMIT 1'))
    if(counter > 0):
        db.cursor.execute(query['update'], query['updatevalues'])
        result['status'] = True
        result['message'] = name+' updated successfully'
    else:
        db.cursor.execute(query['insert'], query['insertvalues'])
        result['status'] = True
        result['message'] =  'New '+name+' Added successfully'

    return result
