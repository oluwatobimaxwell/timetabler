from django.http import HttpResponse, HttpResponseRedirect
from admin.models import Functions
from enrollment.models import Enrolment
from lecturers_mgt.models import Lecturers
from courses_mgt.models import Course
from venues_mgt.models import Venue
from constraints.models import UserConstraints
import pandas as pd
import numpy as np
import datetime
from functools import reduce
from operator import or_, and_


studentLogs = {}
lecturerLogs = {}

def getLecturer(QueryValue):
    return Course.objects.get(code=QueryValue).lecturers


def courseunit(QueryValue):
    return Course.objects.get(code=QueryValue).coursehourperweek

def visitingLecturer(QueryValue):
    visiting = []
    for id in QueryValue:
        visiting.append(Lecturers.objects.get(code=id).visiting)
    return visiting


def lecPriority(QueryValue):
    priority = []
    for id in QueryValue:
        priority.append(Lecturers.objects.get(code=id).priorityNumber.type)

    sumx =  sum(priority)
    lenx =  len(priority) if len(priority) > 0 else 1
    return sumx/lenx
    return priority;

def timeDiff(time1,time2):
    t1h = int(time1.hour)
    t1m = int(time1.minute)
    t2h = int(time2.hour)
    t2m = int(time2.minute)
    dif = (t1h*60 + t1m)-(t2h*60 + t2m)
    return dif

def addminIntTotime(starttime, number):
    return datetime.timedelta(hours = starttime.hour, minutes=starttime.minute + number, seconds=starttime.second)

def getFinishedTime(starttime, courseunit):
    x = int(starttime.hour)
    if courseunit >= 3:
        x += 3
    else:
        x += 2
    # print(datetime.strptime(starttime).timestamp())
    return datetime.timedelta(hours = x, minutes=starttime.minute, seconds=starttime.second)

def getVenues(department, level):
    venues = list(Venue.objects.filter(reservedDepartment__contains=str(department), reservedLevel__contains=str(level)))
    return venues


def getLecturerAvail(QueryValue):
    period = []
    if len(QueryValue) > 0:
        data = dict(Lecturers.objects.values('mon','monFrom','monTo','tue','tueFrom','tueTo','wed','wedFrom','wedTo','thu','thuFrom','thuTo','fri','friFrom','friTo','sat','satFrom','satTo').get(code=QueryValue[0]))
        period = [[data['mon'], data['monFrom'],  data['monTo'], 'mon'],
                  [data['tue'], data['tueFrom'], data['tueTo'], 'tue'],
                  [data['wed'], data['wedFrom'], data['wedTo'], 'wed'],
                  [data['thu'], data['thuFrom'], data['thuTo'], 'thu'],
                  [data['fri'], data['friFrom'], data['friTo'], 'fri'],
                  [data['sat'], data['satFrom'], data['satTo'], 'sat']]
        return(period)
    else:
        return([])

def constraints(args):
    data = UserConstraints.objects.values().get(id=1)
    return(data[args])

def getStudentNotFreePeriods(df, student):
    studentNotFree = []
    df = df[(df['student'] == student) & (df['starttime'] != '')]
    for day in df.itertuples():
        if day.starttime != '':
            studentNotFree.append([True, day.starttime, day.endtime, day.lectureday])

    return studentNotFree


def changetostring(arg):
    return str(arg)

def time_plus(time, timedelta):
    start = datetime.datetime(
        2000, 1, 1,
        hour=time.hour, minute=time.minute, second=time.second)
    end = start + timedelta
    return end.time()

def getLecturerFreePeriods(df, lecavail, lecturers):
    lecturerFree = []
    if len(lecturers) > 0:
        df_lect = df[df['lecturers'].str[0] == lecturers[0]]
        if len(df_lect) > 0:
            for day in lecavail:
                if day[0] == True:
                    today = []
                    df_lect_today = df_lect[df_lect['lectureday'] == day[3]]
                    if len(df_lect_today) > 0:
                        df_min = df_lect_today.sort_values(by=['starttime'], ascending=False)
                        df_max = df_lect_today.sort_values(by=['endtime'], ascending=True)

                        if timeDiff(day[2], df_max['endtime'].iloc[-1]) > 59:
                            today = [True, df_max['endtime'].iloc[-1], day[2], day[3]]

                    else:
                        today = day

                    lecturerFree.append(today)
        else:
            print('No lecturer')
    return lecturerFree


def evaluateSchedule(courseunit, lecturerFree, studentNotFree, studentclass):
    schedule = {
        'start': '',
        'end': '',
        'day': '',
        'status': False
    }

    for lect_now_avail in lecturerFree:
        if len(lect_now_avail) > 0:
            if len(studentNotFree) > 0:
                for std in studentNotFree:
                    # check same day ... same lecturer can also be checked here
                    # if std[3] == lect_now_avail[3]:

                    stdnextstart = time_plus(std[2], datetime.timedelta(minutes = constraints('StuMinBtwClasses')))

                    if timeDiff(lect_now_avail[2],stdnextstart) >= courseunit*60:

                        for thisclass in studentLogs[studentclass]:
                            if thisclass[2] != lect_now_avail[3]:
                                schedule['start'] = stdnextstart
                                schedule['end'] = time_plus(stdnextstart, datetime.timedelta(minutes = (courseunit * 60)))
                                schedule['day'] = lect_now_avail[3]
                                schedule['status'] = True
                                break
                            else:
                                continue

                        studentLogs[studentclass].append([schedule['start'], schedule['end'], schedule['day']])
                        break

            else:
                if len(studentLogs[studentclass]) > 0:
                    for thisclass in studentLogs[studentclass]:
                        if thisclass[2] != lect_now_avail[3]:
                            schedule['start'] = lect_now_avail[1]
                            schedule['end'] = time_plus(lect_now_avail[1], datetime.timedelta(minutes = (courseunit * 60)))
                            schedule['day'] = lect_now_avail[3]
                            schedule['status'] = True
                            studentLogs[studentclass].append([schedule['start'], schedule['end'], schedule['day']])
                            break
                        else:
                            continue
                    break
                else:
                    schedule['start'] = lect_now_avail[1]
                    schedule['end'] = time_plus(lect_now_avail[1], datetime.timedelta(minutes = (courseunit * 60)))
                    schedule['day'] = lect_now_avail[3]
                    schedule['status'] = True
                    studentLogs[studentclass].append([schedule['start'], schedule['end'], schedule['day']])
                    break

    return schedule

class Generator():

    def startgen(gendata):

        # define schedule log


        result = '<div class="alert alert-success col-12" role="alert"><i class="mdi mdi-checkbox-marked-circle-outline"></i>  '+str(gendata)+' </div>'
        tableCode = gendata['code']
        tableData = pd.DataFrame()
        message = ''

        # start registration data collection
        if gendata['semestername'] != '' and gendata['semestertype'] == '':
            tableData = pd.DataFrame(list(Enrolment.objects.values().filter(session=gendata['session'], semesterName=gendata['semestername']).order_by('course_code_id')))
        elif gendata['semestername'] == '' and int(gendata['semestertype']) > 0:
            tableData = pd.DataFrame(list(Enrolment.objects.values().filter(session=gendata['session'], semesterType=gendata['semestertype']).order_by('course_code_id')))
        # end registration data collection

        # check if there is registration
        if len(tableData) > 0:

            # start data preparation
            df = pd.DataFrame()
            if gendata['semestername'] != '' and gendata['semestertype'] == '':
                df = tableData[['session', 'semesterName', 'course_code_id', 'level', 'department_id']].groupby(['course_code_id']).apply(lambda x: x.tail(1))
                df['groupid'] = df['session']+df['semesterName']+df['course_code_id']

            elif gendata['semestername'] == '' and int(gendata['semestertype']) > 0:
                df = tableData[['session', 'semesterType', 'course_code_id', 'level', 'department_id']].groupby(['course_code_id']).apply(lambda x: x.tail(1))
                df['groupid'] = df['session']+df['semesterType'].astype(str)+df['course_code_id']

            df['student'] = df['department_id']+'-'+df['level'].astype(str)
            df['totalenrol'] = list(tableData['course_code_id'].value_counts().sort_index())
            df['courseunit'] = df['course_code_id'].apply(courseunit)
            df['lecturers'] = df['course_code_id'].apply(getLecturer)
            df['lecpriority'] = df['lecturers'].apply(lecPriority)
            df['visiting'] = df['lecturers'].apply(visitingLecturer)
            df['lecavail'] = df['lecturers'].apply(getLecturerAvail)
            df['lectureday'] = ''
            df['starttime'] = ''
            df['endtime'] = ''
            df['venue'] = ''
            df['status'] = False
            #


            df = df.sort_values(by=['lecpriority'], ascending=False)

            if constraints('visitingLecturer'):
                df = df.sort_values(by=['visiting'], ascending=False)

            # # end data preparation

            # begin generation algorithm

            # # .....NEXT IS HERE.....

            # initialize all log dictionaries
            stdLog = pd.DataFrame()
            stdLog = df[['student']].groupby(['student']).apply(lambda x: x.tail(1))

            for stdclass in stdLog.itertuples():
                studentLogs[stdclass[0][0]] = []


            # print(studentLogs)


            for row in df.itertuples():

                student = row.student
                lecturers = row.lecturers

                # get lecturer free time
                lecturerFree = getLecturerFreePeriods(df, row.lecavail, lecturers)

                # check when student is free in lecturer free time
                studentNotFree = getStudentNotFreePeriods(df, student)

                venue = getVenues(row.department_id, row.level)

                schedule = evaluateSchedule(row.courseunit, lecturerFree, studentNotFree, student)

                df.at[row.Index, 'starttime'] = schedule['start']
                df.at[row.Index, 'endtime'] = schedule['end']
                df.at[row.Index, 'lectureday'] = schedule['day']
                df.at[row.Index, 'status'] = schedule['status']

            df_gen = df[['course_code_id','lecturers', 'student', 'lectureday', 'starttime', 'endtime', 'status']]

            print(df_gen)
            print(studentLogs)

            # end generation algorithm
            # print(sum(df['totalenrol']))
            # dfx = tableData[['level','semesterType']]
            # ds = dfx.T.apply(lambda x: x.nunique(), axis=1)
            # totaltable = (ds['level']*ds['semesterType'])
            # message = '<div class="alert alert-success col-12" role="alert" style="margin-bottom: 0;line-height: 1.2;font-size: 14px;"><i class="mdi mdi-checkbox-marked-circle-outline"></i> '+str(totaltable)+' Timetables has been generated!</div>'

        else:
            message = '<div class="alert alert-danger col-12" role="alert" style="margin-bottom: 0;line-height: 1.2;font-size: 14px;"><i class="mdi mdi-alert-outline" style="font-size: 34px;float: left;margin-right: 15px;margin-top: -10px;"></i> No registration data found for the selected session and semester, please register students for courses and try again!</div>'

        # print(str(tableData[0]['level']))
        return HttpResponse(message)

































from django.http import HttpResponse, HttpResponseRedirect
from admin.models import Functions
from enrollment.models import Enrolment
from lecturers_mgt.models import Lecturers
from courses_mgt.models import Course
from venues_mgt.models import Venue
from constraints.models import UserConstraints
import pandas as pd
import numpy as np
import datetime
from functools import reduce
from operator import or_, and_

def getLecturer(QueryValue):
    return Course.objects.get(code=QueryValue).lecturers


def courseunit(QueryValue):
    return Course.objects.get(code=QueryValue).coursehourperweek

def visitingLecturer(QueryValue):
    visiting = []
    for id in QueryValue:
        visiting.append(Lecturers.objects.get(code=id).visiting)
    return visiting


def lecPriority(QueryValue):
    priority = []
    for id in QueryValue:
        priority.append(Lecturers.objects.get(code=id).priorityNumber.type)

    sumx =  sum(priority)
    lenx =  len(priority) if len(priority) > 0 else 1
    return sumx/lenx
    return priority;

def timeDiff(time1,time2):
    t1h = int(time1.hour)
    t1m = int(time1.minute)
    t2h = int(time2.hour)
    t2m = int(time2.minute)
    dif = (t1h*60 + t1m)-(t2h*60 + t2m)
    return dif

def addminIntTotime(starttime, number):
    return datetime.timedelta(hours = starttime.hour, minutes=starttime.minute + number, seconds=starttime.second)

def getFinishedTime(starttime, courseunit):
    x = int(starttime.hour)
    if courseunit >= 3:
        x += 3
    else:
        x += 2
    # print(datetime.strptime(starttime).timestamp())
    return datetime.timedelta(hours = x, minutes=starttime.minute, seconds=starttime.second)

def getVenues(department, level):
    venues = list(Venue.objects.filter(reservedDepartment__contains=str(department), reservedLevel__contains=str(level)))
    return venues


def getLecturerAvail(QueryValue):
    period = []
    if len(QueryValue) > 0:
        data = dict(Lecturers.objects.values('mon','monFrom','monTo','tue','tueFrom','tueTo','wed','wedFrom','wedTo','thu','thuFrom','thuTo','fri','friFrom','friTo','sat','satFrom','satTo').get(code=QueryValue[0]))
        period = [[data['mon'], data['monFrom'],  data['monTo'], 'mon'],
                  [data['tue'], data['tueFrom'], data['tueTo'], 'tue'],
                  [data['wed'], data['wedFrom'], data['wedTo'], 'wed'],
                  [data['thu'], data['thuFrom'], data['thuTo'], 'thu'],
                  [data['fri'], data['friFrom'], data['friTo'], 'fri'],
                  [data['sat'], data['satFrom'], data['satTo'], 'sat']]
        return(period)
    else:
        return([])

def constraints(args):
    data = UserConstraints.objects.values().get(id=1)
    return(data[args])

def getStudentNotFreePeriods(df, student):
    studentNotFree = []
    df = df[(df['student'] == student) & (df['starttime'] != '')]
    for day in df.itertuples():
        if day.starttime != '':
            studentNotFree.append([True, day.starttime, day.endtime, day.lectureday])

    return studentNotFree


def changetostring(arg):
    return str(arg)

def time_plus(time, timedelta):
    start = datetime.datetime(
        2000, 1, 1,
        hour=time.hour, minute=time.minute, second=time.second)
    end = start + timedelta
    return end.time()

def getLecturerFreePeriods(df, lecavail, lecturers):
    lecturerFree = []
    if len(lecturers) > 0:
        df_lect = df[df['lecturers'].str[0] == lecturers[0]]
        if len(df_lect) > 0:
            for day in lecavail:
                if day[0] == True:
                    today = []
                    df_lect_today = df_lect[df_lect['lectureday'] == day[3]]
                    if len(df_lect_today) > 0:
                        df_min = df_lect_today.sort_values(by=['starttime'], ascending=False)
                        df_max = df_lect_today.sort_values(by=['endtime'], ascending=True)

                        if timeDiff(day[2], df_max['endtime'].iloc[-1]) > 59:
                            today = [True, df_max['endtime'].iloc[-1], day[2], day[3]]

                    else:
                        today = day

                    lecturerFree.append(today)
        else:
            print('No lecturer')
    return lecturerFree


def evaluateSchedule(courseunit, lecturerFree, studentNotFree):
    schedule = {
        'start': '',
        'end': '',
        'day': '',
        'status': False
    }

    for lect_now_avail in lecturerFree:
        if len(lect_now_avail) > 0:
            if len(studentNotFree) > 0:
                for std in studentNotFree:
                    # check same day ... same lecturer can also be checked here
                    if std[3] != lect_now_avail[3]:
                        stdnextstart = time_plus(std[2], datetime.timedelta(minutes = constraints('StuMinBtwClasses')))

                        if timeDiff(lect_now_avail[2],stdnextstart) >= courseunit*60:
                            schedule['start'] = stdnextstart
                            schedule['end'] = time_plus(stdnextstart, datetime.timedelta(minutes = (courseunit * 60)))
                            schedule['day'] = lect_now_avail[3]
                            schedule['status'] = True
                            break

            else:
                schedule['start'] = lect_now_avail[1]
                schedule['end'] = time_plus(lect_now_avail[1], datetime.timedelta(minutes = (courseunit * 60)))
                schedule['day'] = lect_now_avail[3]
                schedule['status'] = True
                break

    return schedule

class Generator():

    def startgen(gendata):

        result = '<div class="alert alert-success col-12" role="alert"><i class="mdi mdi-checkbox-marked-circle-outline"></i>  '+str(gendata)+' </div>'
        tableCode = gendata['code']
        tableData = pd.DataFrame()
        message = ''

        # start registration data collection
        if gendata['semestername'] != '' and gendata['semestertype'] == '':
            tableData = pd.DataFrame(list(Enrolment.objects.values().filter(session=gendata['session'], semesterName=gendata['semestername']).order_by('course_code_id')))
        elif gendata['semestername'] == '' and int(gendata['semestertype']) > 0:
            tableData = pd.DataFrame(list(Enrolment.objects.values().filter(session=gendata['session'], semesterType=gendata['semestertype']).order_by('course_code_id')))
        # end registration data collection

        # check if there is registration
        if len(tableData) > 0:

            # start data preparation
            df = pd.DataFrame()
            if gendata['semestername'] != '' and gendata['semestertype'] == '':
                df = tableData[['session', 'semesterName', 'course_code_id', 'level', 'department_id']].groupby(['course_code_id']).apply(lambda x: x.tail(1))
                df['groupid'] = df['session']+df['semesterName']+df['course_code_id']

            elif gendata['semestername'] == '' and int(gendata['semestertype']) > 0:
                df = tableData[['session', 'semesterType', 'course_code_id', 'level', 'department_id']].groupby(['course_code_id']).apply(lambda x: x.tail(1))
                df['groupid'] = df['session']+df['semesterType'].astype(str)+df['course_code_id']

            df['student'] = df['department_id']+'-'+df['level'].astype(str)
            df['totalenrol'] = list(tableData['course_code_id'].value_counts().sort_index())
            df['courseunit'] = df['course_code_id'].apply(courseunit)
            df['lecturers'] = df['course_code_id'].apply(getLecturer)
            df['lecpriority'] = df['lecturers'].apply(lecPriority)
            df['visiting'] = df['lecturers'].apply(visitingLecturer)
            df['lecavail'] = df['lecturers'].apply(getLecturerAvail)
            df['lectureday'] = ''
            df['starttime'] = ''
            df['endtime'] = ''
            df['venue'] = ''
            df['status'] = False
            #


            df = df.sort_values(by=['lecpriority'], ascending=False)

            if constraints('visitingLecturer'):
                df = df.sort_values(by=['visiting'], ascending=False)

            # # end data preparation

            # begin generation algorithm

            # # .....NEXT IS HERE.....
            for row in df.itertuples():

                student = row.student
                lecturers = row.lecturers

                # get lecturer free time
                lecturerFree = getLecturerFreePeriods(df, row.lecavail, lecturers)

                # check when student is free in lecturer free time
                studentNotFree = getStudentNotFreePeriods(df, student)

                venue = getVenues(row.department_id, row.level)

                schedule = evaluateSchedule(row.courseunit, lecturerFree, studentNotFree)

                df.at[row.Index, 'starttime'] = schedule['start']
                df.at[row.Index, 'endtime'] = schedule['end']
                df.at[row.Index, 'lectureday'] = schedule['day']
                df.at[row.Index, 'status'] = schedule['status']

            df_gen = df[['course_code_id','lecturers', 'student', 'lectureday', 'starttime', 'endtime', 'status']]

            print(df_gen)
            # end generation algorithm
            # print(sum(df['totalenrol']))
            # dfx = tableData[['level','semesterType']]
            # ds = dfx.T.apply(lambda x: x.nunique(), axis=1)
            # totaltable = (ds['level']*ds['semesterType'])
            # message = '<div class="alert alert-success col-12" role="alert" style="margin-bottom: 0;line-height: 1.2;font-size: 14px;"><i class="mdi mdi-checkbox-marked-circle-outline"></i> '+str(totaltable)+' Timetables has been generated!</div>'

        else:
            message = '<div class="alert alert-danger col-12" role="alert" style="margin-bottom: 0;line-height: 1.2;font-size: 14px;"><i class="mdi mdi-alert-outline" style="font-size: 34px;float: left;margin-right: 15px;margin-top: -10px;"></i> No registration data found for the selected session and semester, please register students for courses and try again!</div>'

        # print(str(tableData[0]['level']))
        return HttpResponse(message)
