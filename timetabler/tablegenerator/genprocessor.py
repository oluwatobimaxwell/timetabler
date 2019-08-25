from django.http import HttpResponse, HttpResponseRedirect
from admin.models import Functions
from enrollment.models import Enrolment
from lecturers_mgt.models import Lecturers
from courses_mgt.models import Course
from venues_mgt.models import Venue
from constraints.models import UserConstraints
from departments_mgt.models import Department
from .models import TablesGenerated
import pandas as pd
from pandas.testing import assert_frame_equal
import numpy as np
import datetime
from time import sleep
from functools import reduce
from operator import or_, and_
import random
import math
from random import randrange
# get all lecturers
def getLecturer(QueryValue):
    return Course.objects.get(code=QueryValue).lecturers

# get all course units
def courseunit(QueryValue):
    return Course.objects.get(code=QueryValue).coursehourperweek
# get all course type
def getSubjectType(QueryValue):
    return Course.objects.get(code=QueryValue).subjecttype

# get visiting or permanent lecturer status
def visitingLecturer(QueryValue):
    visiting = []
    for id in QueryValue:
        if Lecturers.objects.get(code=id).visiting:
            visiting.append(2)
        else:
            visiting.append(1)
    sumx =  sum(visiting)
    lenx =  len(visiting)
    if lenx > 0:
        return  sumx/lenx
    else:
        return 0


# get lecturer priority or lecturer rank
def lecPriority(QueryValue):
    priority = []
    for id in QueryValue:
        priority.append(Lecturers.objects.get(code=id).priorityNumber.type)

    sumx =  sum(priority)
    lenx =  len(priority)
    if lenx > 0:
        return  sumx/lenx
    else:
        return 0

# calculate time difference in minutes between two time object
def timeDiff(time1,time2):
    t1h = int(time1.hour)
    t1m = int(time1.minute)
    t2h = int(time2.hour)
    t2m = int(time2.minute)
    dif = (t1h*60 + t1m)-(t2h*60 + t2m)
    return dif

# calculate lecture finished time given lecture start time
def getFinishedTime(starttime, courseunit):
    x = int(starttime.hour)
    if courseunit >= 3:
        x += 3
    else:
        x += 2
    return datetime.timedelta(hours = x, minutes=starttime.minute, seconds=starttime.second)

# generate venue for a schedule
def getVenues(department, level):
    venues = list(Venue.objects.filter(reservedDepartment__contains=str(department), reservedLevel__contains=str(level)))
    return venues

# get a lecturer standard free periods
def getLecturerAvail(QueryValue):
    Saturday = False
    if constraints('AssignSaturdays'):
        Saturday = True
    period = []
    if len(QueryValue) > 0:
        data = dict(Lecturers.objects.values('mon','monFrom','monTo','tue','tueFrom','tueTo','wed','wedFrom','wedTo','thu','thuFrom','thuTo','fri','friFrom','friTo','sat','satFrom','satTo').get(code=QueryValue[0]))
        period = [[data['mon'], data['monFrom'],  data['monTo'], 'mon'],
                  [data['tue'], data['tueFrom'], data['tueTo'], 'tue'],
                  [data['wed'], data['wedFrom'], data['wedTo'], 'wed'],
                  [data['thu'], data['thuFrom'], data['thuTo'], 'thu'],
                  [data['fri'], data['friFrom'], data['friTo'], 'fri'],
                  [Saturday and data['sat'], data['satFrom'], data['satTo'], 'sat']]
        if constraints('MuslimWeekPrayer'):
            prayerStart = constraints('MuslimPrayStart')
            prayerEnd = time_plus(constraints('MuslimPrayStart'), datetime.timedelta(minutes = constraints('MuslimPrayDuration')))
            period = [
                [data['mon'], data['monFrom'],  data['monTo'], 'mon'],
                [data['tue'], data['tueFrom'], data['tueTo'], 'tue'],
                [data['wed'], data['wedFrom'], data['wedTo'], 'wed'],
                [data['thu'], data['thuFrom'], data['thuTo'], 'thu'],
                [data['fri'], data['friFrom'], prayerStart, 'fri'],
                [data['fri'], prayerEnd, data['friTo'], 'fri'],
                [Saturday and data['sat'], data['satFrom'], data['satTo'], 'sat']
            ]

        if constraints('AllowDailyBrkTime'):
            breakStart = constraints('DailyBrkStartTime')
            breakEnd = time_plus(constraints('DailyBrkStartTime'), datetime.timedelta(minutes = constraints('DailyBrkDuration')))
            period = [
                [data['mon'], data['monFrom'], breakStart, 'mon'],
                [data['mon'], breakEnd, data['monTo'], 'mon'],
                [data['tue'], data['tueFrom'], breakStart, 'tue'],
                [data['tue'], breakEnd, data['tueTo'], 'tue'],
                [data['wed'], data['wedFrom'], breakStart, 'wed'],
                [data['wed'], breakEnd, data['wedTo'], 'wed'],
                [data['thu'], data['thuFrom'], breakStart, 'thu'],
                [data['thu'], breakEnd, data['thuTo'], 'thu'],
                [data['fri'], data['friFrom'], breakStart, 'fri'],
                [data['fri'], breakEnd, data['friTo'], 'fri'],
                [Saturday and data['sat'], data['satFrom'], breakStart, 'sat'],
                [Saturday and data['sat'], breakEnd, data['satTo'], 'sat']
            ]
        if constraints('AllowDailyBrkTime') and constraints('MuslimWeekPrayer'):
            prayerStart = constraints('MuslimPrayStart')
            prayerEnd = time_plus(constraints('MuslimPrayStart'), datetime.timedelta(minutes = constraints('MuslimPrayDuration')))

            breakStart = constraints('DailyBrkStartTime')
            breakEnd = time_plus(constraints('DailyBrkStartTime'), datetime.timedelta(minutes = constraints('DailyBrkDuration')))
            period = [
                [data['mon'], data['monFrom'], breakStart, 'mon'],
                [data['mon'], breakEnd, data['monTo'], 'mon'],
                [data['tue'], data['tueFrom'], breakStart, 'tue'],
                [data['tue'], breakEnd, data['tueTo'], 'tue'],
                [data['wed'], data['wedFrom'], breakStart, 'wed'],
                [data['wed'], breakEnd, data['wedTo'], 'wed'],
                [data['thu'], data['thuFrom'], breakStart, 'thu'],
                [data['thu'], breakEnd, data['thuTo'], 'thu'],
                [data['fri'], data['friFrom'], prayerStart, 'fri'],
                [data['fri'], prayerEnd, data['friTo'], 'fri'],
                [data['sat'] and Saturday, data['satFrom'], breakStart, 'sat'],
                [data['sat'] and Saturday, breakEnd, data['satTo'], 'sat']
            ]
        return(period)
    else:
        return([])

# get a particular constraint value
def constraints(args):
    data = UserConstraints.objects.values().get(id=1)
    return(data[args])

# change time object to string
def changetostring(arg):
    return str(arg)

# add x-minutes to a time object
def time_plus(time, timedelta):
    start = datetime.datetime(
        2000, 1, 1,
        hour=time.hour, minute=time.minute, second=time.second)
    end = start + timedelta
    return end.time()

# get a particular student group standard free periods
def getStudentTime():

    Saturday = False
    if constraints('AssignSaturdays'):
        Saturday = True

    startLecture = constraints('LectureStartTime')
    endLecture = constraints('LectureCloseTime')
    initialPeriod = [
        [True, startLecture, endLecture, 'mon'],
        [True, startLecture, endLecture, 'tue'],
        [True, startLecture, endLecture, 'wed'],
        [True, startLecture, endLecture, 'thu'],
        [True, startLecture, endLecture, 'fri'],
        [Saturday, startLecture, endLecture, 'sat']
    ]
    if constraints('MuslimWeekPrayer'):
        prayerStart = constraints('MuslimPrayStart')
        prayerEnd = time_plus(constraints('MuslimPrayStart'), datetime.timedelta(minutes = constraints('MuslimPrayDuration')))
        initialPeriod = [
            [True, startLecture, endLecture, 'mon'],
            [True, startLecture, endLecture, 'tue'],
            [True, startLecture, endLecture, 'wed'],
            [True, startLecture, endLecture, 'thu'],
            [True, startLecture, prayerStart, 'fri'],
            [True, prayerEnd, endLecture, 'fri'],
            [Saturday, startLecture, endLecture, 'sat']
        ]

    if constraints('AllowDailyBrkTime'):
        breakStart = constraints('DailyBrkStartTime')
        breakEnd = time_plus(constraints('DailyBrkStartTime'), datetime.timedelta(minutes = constraints('DailyBrkDuration')))
        initialPeriod = [
            [True, startLecture, breakStart, 'mon'],
            [True, breakEnd, endLecture, 'mon'],
            [True, startLecture, breakStart, 'tue'],
            [True, breakEnd, endLecture, 'tue'],
            [True, startLecture, breakStart, 'wed'],
            [True, breakEnd, endLecture, 'wed'],
            [True, startLecture, breakStart, 'thu'],
            [True, breakEnd, endLecture, 'thu'],
            [True, startLecture, breakStart, 'fri'],
            [True, breakEnd, endLecture, 'fri'],
            [Saturday, startLecture, breakStart, 'sat'],
            [Saturday, breakEnd, endLecture, 'sat']
        ]

    if constraints('AllowDailyBrkTime') and constraints('MuslimWeekPrayer'):
        prayerStart = constraints('MuslimPrayStart')
        prayerEnd = time_plus(constraints('MuslimPrayStart'), datetime.timedelta(minutes = constraints('MuslimPrayDuration')))

        breakStart = constraints('DailyBrkStartTime')
        breakEnd = time_plus(constraints('DailyBrkStartTime'), datetime.timedelta(minutes = constraints('DailyBrkDuration')))
        initialPeriod = [
            [True, startLecture, breakStart, 'mon'],
            [True, breakEnd, endLecture, 'mon'],
            [True, startLecture, breakStart, 'tue'],
            [True, breakEnd, endLecture, 'tue'],
            [True, startLecture, breakStart, 'wed'],
            [True, breakEnd, endLecture, 'wed'],
            [True, startLecture, breakStart, 'thu'],
            [True, breakEnd, endLecture, 'thu'],
            [True, startLecture, prayerStart, 'fri'],
            [True, prayerEnd, endLecture, 'fri'],
            [Saturday, startLecture, breakStart, 'sat'],
            [Saturday, breakEnd, endLecture, 'sat']
        ]

    return initialPeriod

# check remaining free periods for a lecturer
def getLecturerFreePeriods(df, lecavail, lecturers, cosperday, minbclass):
    lecturerFree = []
    if len(lecturers) > 0:
        df_lect = df[df['lecturers'].str[0] == lecturers[0]]
        if len(df_lect) > 0:
            for day in lecavail:
                today = []
                df_lect_today = df_lect[df_lect['lectureday'] == day[3]]
                if len(df_lect_today) > 0:
                    if len(df_lect_today) < cosperday:
                        df_min = df_lect_today.sort_values(by=['starttime'], ascending=False)
                        df_max = df_lect_today.sort_values(by=['endtime'], ascending=True)
                        if timeDiff(day[2], df_max['endtime'].iloc[-1]) > 59:
                            startnow = time_plus(df_max['endtime'].iloc[-1], datetime.timedelta(minutes = minbclass))
                            today = [True, startnow, day[2], day[3]]
                else:
                    today = day
                lecturerFree.append(today)
        else:
            print('No lecturer')
    return lecturerFree

# check remaining free period for a group of students
def getStudentNotFreePeriods(df, initialPeriod, student, cosperday, minbclass):
    studentNotFree = []
    df = df[df['student'].str.contains(student)==True]
    if len(df) > 0:
        for day in initialPeriod:
            today = []
            df_std_today = df[df['lectureday'] == day[3]]
            if len(df_std_today) > 0:
                if len(df_std_today) < cosperday:
                    df_min = df_std_today.sort_values(by=['starttime'], ascending=False)
                    df_max = df_std_today.sort_values(by=['endtime'], ascending=True)
                    if timeDiff(day[2], df_max['endtime'].iloc[-1]) > 59:
                        startnow = time_plus(df_max['endtime'].iloc[-1], datetime.timedelta(minutes = minbclass))
                        today = [True, startnow, day[2], day[3]]

            else:
                today = day
            studentNotFree.append(today)
    return studentNotFree

# schedule a meeting for a lecturer, a group of student in a common time space
def evaluateSchedule(df_ven, df_veri, visiting, lecturers_id, students_id, courseunit, lecturerFree, studentNotFree, venueData, metadata, trackrecord):
    schedule = {
        'start': datetime.time(0, 0, 0),
        'end': datetime.time(0, 0, 0),
        'day': '',
        'venue': '',
        'status': False,
        'comment': ''
    }
    venueWeights = {
        'Type': 7,
        'Size': 5,
        'Level': 3,
        'Department': 10,
        'Faculty': 15,
        'Day': 2,
    }

    random.shuffle(studentNotFree)
    random.shuffle(lecturerFree)

    # print(studentNotFree)
    # print(lecturerFree)

    scheduleData = []
    for stdDay, lectDay in zip(studentNotFree, lecturerFree):
        if len(stdDay) > 0 and len(lectDay) > 0:
            if stdDay[0] and lectDay[0]:
                lecPeriod = courseunit*60
                if lecPeriod <= timeDiff(stdDay[2], stdDay[1]) and lecPeriod <= timeDiff(lectDay[2], lectDay[1]):
                    if lectDay[1] >= stdDay[1]:
                        A = lectDay[1]
                        B = time_plus(lectDay[1], datetime.timedelta(minutes = lecPeriod))
                        C = lectDay[3]
                        D = True
                        E = 'Assigned'
                        scheduleData = [A,B,C]

                        recordTracker = 0
                        if len(trackrecord) > 0:
                            for value in trackrecord:
                                if C == value[0] and A == value[1]:
                                    recordTracker += 1
                        if recordTracker > 0:
                            continue
                        else:

                            if verifySchedule(df_veri, A, B, C, D, lecturers_id, students_id):
                                schedule['start'] = A
                                schedule['end'] = B
                                schedule['day'] = C
                                schedule['status'] = D
                                schedule['comment'] = E
                                trackrecord.append([C,A,B])
                                break
                    else:
                        A = stdDay[1]
                        B = time_plus(stdDay[1], datetime.timedelta(minutes = lecPeriod))
                        C = stdDay[3]
                        D = True
                        E = 'Assigned'
                        scheduleData = [A,B,C]

                        recordTracker = 0
                        if len(trackrecord) > 0:
                            for value in trackrecord:
                                if C == value[0] and A == value[1]:
                                    recordTracker += 1
                        if recordTracker > 0:
                            continue
                        else:
                            if verifySchedule(df_veri, A, B, C, D, lecturers_id, students_id):
                                schedule['start'] = A
                                schedule['end'] = B
                                schedule['day'] = C
                                schedule['status'] = D
                                schedule['comment'] = E
                                trackrecord.append([C,A,B])
                                break

                else:
                    continue

    if not(schedule['status']):
        if metadata < 7 and len(lecturers_id)>0:
            if metadata < 4:
                return evaluateSchedule(df_ven, df_veri, visiting, lecturers_id, students_id, courseunit, lecturerFree, studentNotFree, venueData, metadata+1, trackrecord)
            else:
                if not(visiting) or not(visiting and constraints('restrictVisiting')):
                    return evaluateSchedule(df_ven, df_veri, visiting, lecturers_id, students_id, courseunit, getStudentTime(), studentNotFree, venueData, metadata+1, trackrecord)
        else:
            if metadata >= 4:
                schedule['comment'] = 'No free time space found, for this lecturer and the students.'
            else:
                schedule['comment'] = getReasonForNotSchedule(df_veri, lecturers_id, students_id,scheduleData, courseunit, lecturerFree, studentNotFree)
    else:
        if metadata > 3:
            schedule['comment'] = 'Lecturer may not be available on this day.'
    schedule['venue'] = scheduleMeetingVenue(df_ven, venueData, schedule['start'], schedule['end'], schedule['day'], 0, venueWeights)

    if schedule['status'] == False and len(trackrecord) > 0:
        if verifySchedule(df_veri, trackrecord[1], trackrecord[2], trackrecord[0], True, lecturers_id, students_id):
            schedule['start'] = trackrecord[1]
            schedule['end'] = trackrecord[2]
            schedule['day'] = trackrecord[0]
            schedule['status'] = True
            schedule['comment'] = 'Assigned'

    return schedule

# verify a scheduled class and confirm no clashing
def verifySchedule(df, start_time, end_time, lecturer_day, status, lecturers_id, students_id):
    verifier = [False, False]
    if len(lecturer_day) > 0:
        dfs = df[(df['student'].str.contains(students_id)==True)&(df['lectureday'] == lecturer_day)]
        if len(dfs) < constraints('StuMaxClassPerDay'):
            if len(dfs) > 0:
                checker = 0
                for row in dfs.itertuples():
                    if (start_time >= row.starttime and start_time <= row.endtime) or (end_time >= row.starttime and end_time <= row.endtime):
                        checker += 1
                        break
                if checker == 0:
                    verifier[0] = True
            else:
                verifier[0] = True

        dfl = df[(df['lecturers'].str[0] == lecturers_id[0])&(df['lectureday'] == lecturer_day)]
        if len(dfl) < constraints('LecMaxClassPerDay'):
            if len(dfl) > 0:
                checker = 0
                for row in dfl.itertuples():
                    if (start_time >= row.starttime and start_time <= row.endtime) or (end_time >= row.starttime and end_time <= row.endtime):
                        checker += 0
                        break
                if checker == 0:
                    verifier[1] = True
            else:
                verifier[1] = True

        if verifier[0] and verifier[1]:
            verichecker = False
            Break = False
            Prayer = False
            if constraints('AllowDailyBrkTime'):
                Break = True
                breakStart = constraints('DailyBrkStartTime')
                breakEnd = time_plus(constraints('DailyBrkStartTime'), datetime.timedelta(minutes = constraints('DailyBrkDuration')))
                if end_time <= breakStart or start_time >= breakEnd:
                    verichecker = True

            if constraints('MuslimWeekPrayer') and lecturer_day == 'fri':
                Prayer = True
                prayerStart = constraints('MuslimPrayStart')
                prayerEnd = time_plus(constraints('MuslimPrayStart'), datetime.timedelta(minutes = constraints('MuslimPrayDuration')))
                if end_time <= prayerStart or start_time >= prayerEnd:
                    verichecker = True

            if Break:
                return verichecker and Break
            elif Prayer:
                return verichecker and Prayer
            elif Break and Prayer:
                return verichecker and Break and Prayer
            else:
                return True

        else:
            return False
    else:
        return False


# get reason why schedule is not made
def getReasonForNotSchedule(df, lecturers_id, students_id, scheduleData, courseunit, lecturerFree, studentNotFree):
    reason = 'No space for both student & lecturer to meet'
    studentReason = ''
    lecturerReason = ''
    # checking for lecturer reason
    if len(lecturers_id) <= 0:
        reason =  'No Lecturer'
    else:
        if len(scheduleData) > 0:
            dfl = df[(df['lecturers'].str[0] == lecturers_id[0])&(df['lectureday'] == scheduleData[2])]
            if len(dfl) > 0:
                for row in dfl.itertuples():
                    if row.starttime < scheduleData[1] or row.endtime > scheduleData[0]:

                        lecturerReason = 'Lect: Having another class['+str(row.course_code_id)+']'
                        break
            else:
                lecAvailablePeriod = getLecturerAvail(lecturers_id)
                dayCheck = True
                for lecavail in lecAvailablePeriod:
                    if lecavail[3] == scheduleData[2]:
                        if lecavail[0]:
                            lecturerReason = 'Lecturer currently busy!'
                        else:
                            lecturerReason = 'Lecturer isn\'t available today!'
                        break;

            dfs = df[(df['student'].str.contains(students_id)==True)&(df['lectureday'] == scheduleData[2])]
            if len(dfl) > 0:
                for row in dfs.itertuples():
                    if row.starttime < scheduleData[1] or row.endtime > scheduleData[0]:

                        studentReason = 'Std: Having another class['+str(row.course_code_id)+']'
                        break
            else:
                stdAvailablePeriod = getStudentTime()
                dayCheck = True
                for stdavail in stdAvailablePeriod:
                    if stdavail[3] == scheduleData[2]:
                        if stdavail[0]:
                            studentReason = 'Students currently busy!'
                        else:
                            studentReason = 'Students aren\'t available today!'
                        break;

    if studentReason != '' or lecturerReason != '':
        reason = studentReason +', '+lecturerReason

    return reason


def scheduleMeetingVenue(df, venueData, meetstart, meetend, meetday, metadata, Weights):
    # get all venues
    VenueDB = venueData['VenueDB']
    Lecturer = venueData['lecturer']
    Student = venueData['student']
    Size = venueData['size']
    Dpt = venueData['dpt']
    Fct = venueData['fac']
    Level = venueData['level']
    Type = venueData['type']
    Course = venueData['course']

    venueType  = []
    if Type == 0:
        venueType = [0,1,3]
    elif Type == 1:
        venueType = [2,3]
    else:
        venueType = [0,1,2,3]

    scheduleVenue = ''
    freeVenues = []

    if len(VenueDB) > 0:
        for thisvenue in VenueDB.itertuples():
            if len(df) > 0:
                dfc = df[(df['venue'] == thisvenue.code)&(df['lectureday'] == meetday)&(((df['starttime'] >=  meetstart)&(df['starttime'] <=  meetend))|((df['endtime'] >=  meetstart)&(df['endtime'] <=  meetend)))]
                if len(dfc) > 0:
                    continue
                else:
                    freeVenues.append([thisvenue.code, thisvenue.type, thisvenue.capacity, thisvenue.reservedLevel, thisvenue.reservedFaculty, thisvenue.reservedDepartment, thisvenue.reservedDays])
            else:
                freeVenues.append([thisvenue.code, thisvenue.type, thisvenue.capacity, thisvenue.reservedLevel, thisvenue.reservedFaculty, thisvenue.reservedDepartment, thisvenue.reservedDays])

    Aw = Weights['Type']
    Bw = Weights['Size']
    Cw = Weights['Level']
    Dw = Weights['Department']
    Ew = Weights['Faculty']
    Fw = Weights['Day']
    preferredVenues = {}
    if len(freeVenues) > 0:
        for freev in freeVenues:
            A = int(freev[1] in venueType)
            B = int(Size <= freev[2])
            C = int(Level in freev[3])
            D = int(Dpt in freev[5])
            E = int(Fct in freev[4])
            F = int(meetday in freev[6])
            preferredVenues[freev[0]] = A*Aw + B*Bw + C*Cw + D*Dw + E*Ew + F*Fw

        scheduleVenue =  max(preferredVenues, key=preferredVenues.get)
    if scheduleVenue == '' and metadata < 4:

        if metadata < 4:
            # Weights[metadata] = random.randint(metadata,7)
            # Weights[4] = Weights[4]+1
            # random.shuffle(Weights)
            return scheduleMeetingVenue(df, venueData, meetstart, meetend, meetday, metadata+1, Weights)
        else:
            scheduleVenue = 'No Free Venue'

    return scheduleVenue

def getUniquemembers(mylist):
    return list(sorted(set(mylist)))

# generator class
class Generator():

    # initiate time table generation
    def startgen(gendata, dbinstance):
        genStartat = datetime.datetime.now()
        print('START TIME: ', genStartat)
        result = '<div class="alert alert-success col-12" role="alert"><i class="mdi mdi-checkbox-marked-circle-outline"></i>  '+str(gendata)+' </div>'
        tableCode = dbinstance #gendata['code']
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
            venuesDF = pd.DataFrame(list(Venue.objects.values()))
            # start data preparation
            df = pd.DataFrame()
            if gendata['semestername'] != '' and gendata['semestertype'] == '':
                df = tableData[['session', 'semesterName', 'semesterType', 'course_code_id', 'level', 'department_id']].groupby(['course_code_id']).apply(lambda x: x.tail(1))
                df['groupid'] = df['session']+df['semesterName']+df['course_code_id']

            elif gendata['semestername'] == '' and int(gendata['semestertype']) > 0:
                df = tableData[['session', 'semesterType', 'course_code_id', 'level', 'department_id']].groupby(['course_code_id']).apply(lambda x: x.tail(1))
                df['groupid'] = df['session']+df['semesterType'].astype(str)+df['course_code_id']



            tableData['students_x'] = tableData['department_id']+'-'+tableData['level'].astype(str)+'-'+tableData['semesterType'].astype(str)
            studentGroup = tableData.groupby('course_code_id')['students_x'].agg(lambda x: x[x != 0].tolist()).reset_index()
            studentGroup['student'] = studentGroup['students_x'].apply(getUniquemembers)

            def getStudents(cousecode):
                return ",".join(list(studentGroup.loc[studentGroup['course_code_id']==cousecode]['student'])[0])

            df['student'] = df['course_code_id'].apply(getStudents)
            df['totalenrol'] = list(tableData['course_code_id'].value_counts().sort_index())
            df['courseunit'] = df['course_code_id'].apply(courseunit)
            df['lecturers'] = df['course_code_id'].apply(getLecturer)
            df['lecpriority'] = df['lecturers'].apply(lecPriority)
            df['visiting'] = df['lecturers'].apply(visitingLecturer)
            df['lecavail'] = df['lecturers'].apply(getLecturerAvail)
            df['subjecttype'] = df['course_code_id'].apply(getSubjectType)
            df['lectureday'] = ''
            df['starttime'] = datetime.time(0,0)
            df['endtime'] = datetime.time(0,0)
            df['venue'] = ''
            df['status'] = False
            df['comment'] = 'Not Assigned'
            #

            df = df.sort_values(by=['lecpriority'], ascending=False)
            if constraints('visitingLecturer'):
                df = df.sort_values(by=['lecpriority', 'visiting'], ascending=[False,False])

            # # end data preparation

            # begin generation algorithm
            # print(df[['visiting', 'lecpriority']])
            # # .....NEXT IS HERE.....
            lineindex  = 0
            scheduleRegistry = []
            for row in df.itertuples():
                assertPd = df
                student = row.student.split(",")
                lecturers = row.lecturers
                for pos, studentx in enumerate(student):
                    if not(row.groupid in scheduleRegistry):
                        print(str(lineindex),' - ' ,row.groupid)
                        print('REGISTRY LENGTH: ', str(len(scheduleRegistry)))

                        venuedfs = df[df['venue'] != '']
                        approvedschedules = df[df['status'] == True]
                        lecturerFree = getLecturerFreePeriods(df, row.lecavail, lecturers, constraints('LecMaxClassPerDay'), constraints('LecMinBtwClasses'))
                        # check when student is free in lecturer free time
                        studentNotFree = getStudentNotFreePeriods(df, getStudentTime(),  studentx, constraints('StuMaxClassPerDay'), constraints('StuMinBtwClasses'))
                        venueData = {'VenueDB': venuesDF,'lecturer': row.lecturers,'student': studentx,
                            'size': row.totalenrol,'dpt': row.department_id,'fac': Functions.getDptFac(row.department_id),
                            'level': row.level,'type': row.subjecttype,'course': row.course_code_id,}

                        schedule = evaluateSchedule(venuedfs, approvedschedules, row.visiting, lecturers, studentx, row.courseunit, lecturerFree, studentNotFree, venueData, 0, [])

                        if len(df[(df['lectureday'] == schedule['day'])&
                              (((df['starttime'] >= schedule['start'])&(df['starttime'] <= schedule['end']))|
                              ((df['endtime'] >= schedule['start'])&(df['endtime'] >= schedule['end'])))&
                              (df['student'].str.contains(studentx)==True)]) == 0:

                            df.at[row.Index, 'starttime'] = schedule['start']
                            df.at[row.Index, 'endtime'] = schedule['end']
                            df.at[row.Index, 'lectureday'] = schedule['day']
                            df.at[row.Index, 'status'] = schedule['status']
                            df.at[row.Index, 'venue'] = schedule['venue']
                            df.at[row.Index, 'comment'] = schedule['comment']
                            # print(datetime.datetime.now())
                            scheduleRegistry.append(row.groupid)
                            lineindex+=1

                    else:
                        break



            df_gen = df[['groupid', 'course_code_id','lecturers', 'student', 'totalenrol', 'lectureday', 'starttime', 'endtime', 'venue', 'status', 'department_id', 'comment']]

            for schedule in df_gen.itertuples():
                # check if record exist

                venueinstance = None
                try:
                    venueinstance = Venue.objects.get(code=schedule.venue)
                except Venue.DoesNotExist:
                    venueinstance = None

                departmentinstance = None
                try:
                    departmentinstance = Department.objects.get(code=schedule.department_id)
                except Department.DoesNotExist:
                    departmentinstance = None


                lecturerx = ''
                if len(schedule.lecturers) > 0 and schedule.lecturers[0] != '':
                    lecturerx = schedule.lecturers[0]

                courseinstance = Course.objects.get(code=schedule.course_code_id)

                defaults = {
                    'totalenrol':schedule.totalenrol,
                    'starttime':schedule.starttime,
                    'endtime':schedule.endtime,
                    'lecturers':lecturerx,
                    'lectureday':schedule.lectureday,
                    'code':tableCode,
                    'venue':venueinstance,
                    'course':courseinstance,
                    'remarks':schedule.comment,
                    'status':schedule.status,
                    'students':schedule.student,
                    'department': departmentinstance,
                }
                try:
                    obj = TablesGenerated.objects.get(groupid=schedule.groupid)
                    for key, value in defaults.items():
                        setattr(obj, key, value)
                    obj.save()

                except TablesGenerated.DoesNotExist:
                    new_values = {'groupid': schedule.groupid}
                    new_values.update(defaults)
                    obj = TablesGenerated(**new_values)
                    obj.save()


            totaltable = len(df_gen)
            successSchedule = len(df_gen[df_gen['status'] == True])
            successVenue = 0 #len(df_gen[['venue']])
            print('NO VENUE: ',str(len(df_gen[['totalenrol','lectureday', 'starttime', 'endtime', 'venue', 'status','venue']].loc[df_gen['venue'] == ''])))
            print(df_gen[['totalenrol','lectureday', 'starttime', 'endtime', 'venue', 'status','venue']].loc[df_gen['venue'].str.contains('V')==False])
            totalTimeSpentgen = timeDiff(datetime.datetime.now(), genStartat)*60
            print('FINISHED TIME: ', datetime.datetime.now())
            print('TIME SPENT: ', totalTimeSpentgen, 'seconds')
            # print(df_gen)
            message = '<div class="alert alert-success col-12" role="alert" style="margin-bottom: 0;line-height: 1.2;font-size: 14px;"><i class="mdi mdi-checkbox-marked-circle-outline"></i> '+str(successSchedule)+' out of '+str(totaltable)+' courses have been successfully scheduled. '+str(successVenue)+' have venues. Click view Tables to manage timetable!</div>'
        else:
            message = '<div class="alert alert-danger col-12" role="alert" style="margin-bottom: 0;line-height: 1.2;font-size: 14px;"><i class="mdi mdi-alert-outline" style="font-size: 34px;float: left;margin-right: 15px;margin-top: -10px;"></i> No registration data found for the selected session and semester, please register students for courses and try again!</div>'

        # print(str(tableData[0]['level']))
        return HttpResponse(message)


def getGeneratedTable(scheduler):
    dfmain = pd.DataFrame(list(TablesGenerated.objects.values().filter(code=scheduler).order_by('status')))
    dfmain.rename(columns={'students': 'student'}, inplace=True)
    return dfmain

class ManualScheduler():

    def getAvailableMatches(scheduler, scheduleid, venueid):
        try:
            scheduledata = TablesGenerated.objects.get(groupid=scheduleid)
            studentsy = scheduledata.students.split(",")
            lecturersy = scheduledata.lecturers.split(",")
            coursecode = scheduledata.course.code

            schedulerTable = getGeneratedTable(scheduler)
            studentAvailability = {}
            lectuerAvailability = {}
            venueAvailability = {}

            for studentx in studentsy:
                studentAvailable = getStudentNotFreePeriods(schedulerTable, getStudentTime(),  studentx, constraints('StuMaxClassPerDay'), constraints('StuMinBtwClasses'))
                suggestion = []
                for freespace in studentAvailable:
                    if len(freespace) > 0:
                        if freespace[0]:
                            suggestion.append(freespace)
                studentAvailability[studentx] = suggestion

            for lecturersx in lecturersy:
                lecturerFree = getLecturerFreePeriods(schedulerTable, getLecturerAvail([lecturersx]), lecturersx, constraints('LecMaxClassPerDay'), constraints('LecMinBtwClasses'))
                # thisLecturerTime =
                # lecturerFree = getLecturerFreePeriods(schedulerTable, getStudentTime(), lecturersx, constraints('LecMaxClassPerDay'), constraints('LecMinBtwClasses'))
                print(lecturerFree)
                suggestion = []
                for freespace in lecturerFree:
                    if len(freespace) > 0:
                        if freespace[0]:
                            suggestion.append(freespace)
                lectuerAvailability[lecturersx] = suggestion

            


            return venueid.code
        except TablesGenerated.DoesNotExist:
            return 'Invalid ID, try again with a valid ID'
