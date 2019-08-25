from django.shortcuts import render
from admin.models import Functions
from django.shortcuts import redirect
from django.views.decorators.http import require_POST, require_GET
from django.http import HttpResponse, HttpResponseRedirect
from .forms import  generateForm, manualSchedulerForm
from .genprocessor import Generator, ManualScheduler
from .models import TableRegister, TablesGenerated
import pandas as pd
from courses_mgt.models import Course
from lecturers_mgt.models import Lecturers
from venues_mgt.models import Venue
from departments_mgt.models import Department
import datetime

# Create your views here.
def getTableRegistry(tableId, info):
    result = ''
    if info == 'session':
        result = TableRegister.objects.get(code=tableId).session
    elif info == 'gendate':
        result = TableRegister.objects.get(code=tableId).gendate
    elif info == 'semestername':
        result = TableRegister.objects.get(code=tableId).semestername
    elif info == 'semestertype':
        result = TableRegister.objects.get(code=tableId).semestertype
    elif info == 'totalgen':
        result = TablesGenerated.objects.values('students').distinct().count()

    return result

def getSemester(ses):
    if ses == '1':
        return '1st'
    else:
        return '2nd'

def countStudentsGroupCourses(QueryValue):
    totalCourse = TablesGenerated.objects.filter(students__contains=QueryValue).count()
    totalSchedule = TablesGenerated.objects.filter(students__contains=QueryValue, status=1).count()
    return {
        'courses': totalCourse,
        'scheduled': totalSchedule
    }


def getCourseData(QueryValue, info):
    try:
        return Course.objects.get(code=QueryValue).name
    except Course.DoesNotExist:
        return QueryValue

def getCourseLecturer(QueryValue, info):
    try:
        return Lecturers.objects.get(code=QueryValue).name
    except Lecturers.DoesNotExist:
        return QueryValue

def getCourseVenue(QueryValue, info):
    try:
        return Venue.objects.get(code=QueryValue).name
    except Venue.DoesNotExist:
        return QueryValue

def getCourseDataScheduler(studentgroupid):
    course = {}

    try:
        data = TablesGenerated.objects.get(groupid=studentgroupid)
        course['code'] = data.course.code
        course['title'] = data.course.name
        course['lecturername'] = getCourseLecturer(data.lecturers, 'name')
        course['lecturercode'] = data.lecturers
        # TO BE CONTINUE
        course['studentgroup'] = []
        for std in filter(None, data.students.split(",")):
            # print(std)
            course['studentgroup'].append(str(std.split("-")[1])+'-'+getTableDepartment(std.split("-")[0], 'name'))

        course['remarks'] = data.remarks
    except TablesGenerated.DoesNotExist:
        course['code'] = '-'
        course['title'] = '-'
        course['lecturername'] = '-'
        course['lecturercode'] = '-'
        course['studentgroup'] = '-'
        course['remarks'] = '-'

    return course


def getTableDepartment(QueryValue, info):
    try:
        if info == 'name':
            return Department.objects.get(code=QueryValue).name
        elif info == 'fac':
            return Department.objects.get(code=QueryValue).faculty.name

    except Department.DoesNotExist:
        return QueryValue

def getFullDay(day):
    if day == 'mon':
        return 'Monday'
    elif day == 'tue':
        return 'Tuesday'
    elif day == 'wed':
        return 'Wednesday'
    elif day == 'thu':
        return 'Thursday'
    elif day == 'fri':
        return 'Friday'
    elif day == 'sat':
        return 'Saturday'
    elif day == 'sun':
        return 'Sunday'
    else:
        return '<i class="mdi mdi-alert-decagram-outline text-danger"></i>'

def formatTime(timevalue):
    if timevalue == datetime.time(0,0):
        return '<i class="mdi mdi-alert-decagram-outline text-danger"></i>'
    else:
        return timevalue.strftime("%I:%M %p")

def getRemarks(remarks, status, venue):
    if not(status):
        return '<span class="text-danger" style="font-size: 11px;"> <i class="mdi mdi-alert-circle"></i> '+remarks.capitalize()+'</span>'
    else:
        if venue == None:
            return '<span class="text-warning" style="font-size: 11px;"> <i class="mdi mdi-alert-decagram"></i>'+remarks.capitalize()+'</span>'
        else:
            if remarks == 'Assigned':
                return '<span class="text-success" style="font-size: 11px;"> <i class="mdi mdi-check-circle"></i>'+remarks.capitalize()+'</span>'
            else:
                return '<span class="text-primary" style="font-size: 11px;"> <i class="mdi mdi-check-circle"></i>'+remarks.capitalize()+'</span>'


def index(request):
    if request.user.is_authenticated:

        context = {}

        scheduler=request.GET.get("viewscheduler", None)
        if scheduler == None:
            table_groups = list(TableRegister.objects.values())
            group_list = []
            rownumber = 1
            for table in table_groups:
                table['row'] = rownumber
                table['count'] = 20
                table['status'] = '<i class="mdi mdi-alert-circle text-warning"></i>'
                table['semestertype'] = Functions.getSemesterName(table['semestertype'])
                group_list.append(table)
                rownumber += 1

            context = {
                'table_groups': group_list,
                'semesterRequire': Functions.getSemesterReq(),
                'pagedata':{
                    'pageicon':'animation',
                    'pagetitle':'Home: Schedulers',
                }
            }
            return render(request, 'admin/generator/index.html', context)

        else:
            studentgroup=request.GET.get("studentgroup", None)
            if studentgroup == None:
                style=request.GET.get("viewstyle", None)
                if style == None:
                    dfmain = pd.DataFrame(list(TablesGenerated.objects.values('students', 'department_id').filter(code=scheduler).order_by('department_id')))
                    df = dfmain[['students', 'department_id']].groupby(['students']).apply(lambda x: x.tail(1))
                    df['totalstudents'] = list(dfmain['students'].value_counts().sort_index())
                    # print(df)
                    groupListString = ''
                    groupList = list(TablesGenerated.objects.values('students', 'department_id').filter(code=scheduler))
                    for grp in groupList:
                        groupListString = groupListString+','+grp['students']
                        # print(grp)
                    groupListString = groupListString.split(",")
                    groupListString = list(sorted(set(groupListString)))
                    groupListString = filter(None, groupListString)
                    group_list = []
                    rownumber = 1

                    for group in groupListString:
                        print(group)
                        table = {}
                        table['row'] = rownumber
                        table['scheduler'] = scheduler
                        table['students'] = group
                        table['faculty'] = getTableDepartment(group.split("-")[0],'fac')
                        table['department'] = getTableDepartment(group.split("-")[0],'name')
                        table['level'] = group.split("-")[1]+'-Level'
                        table['courses'] = countStudentsGroupCourses(group)['courses']
                        table['scheduled'] = countStudentsGroupCourses(group)['scheduled']
                        table['status'] = '<i class="mdi mdi-alert-circle text-danger"></i>'
                        if table['scheduled'] == table['courses']:
                            table['status'] = '<i class="mdi mdi-checkbox-marked-circle text-success"><span style="display:none">4</span></i>'
                        elif table['scheduled']/table['courses'] > 0.6:
                            table['status'] = '<i class="mdi mdi-alert-circle text-warning"><span style="display:none">3</span></i>'
                        #
                        table['semester'] = '<i class="mdi mdi-numeric-2-circle text-info" style="font-size: 20px;"><span style="display:none">2</span></>'
                        if group.split("-")[2] == '1':
                            table['semester'] = '<i class="mdi mdi-numeric-1-circle text-primary" style="font-size: 20px;"><span style="display:none">1</span></>'

                        # table['semestertype'] = Functions.getSemesterName(table['semestertype'])
                        group_list.append(table)
                        rownumber += 1

                    context = {
                        'table_groups_dpt': group_list,
                        'semesterRequire': Functions.getSemesterReq(),
                        'pagedata':{
                            'pageicon':'animation',
                            'pagetitle':'Timetable Generator',
                        }
                    }
                    return render(request, 'admin/generator/index.html', context)
                else:
                    dfmain = pd.DataFrame(list(TablesGenerated.objects.values('groupid', 'totalenrol', 'students', 'starttime', 'endtime', 'lecturers', 'lectureday', 'venue', 'course', 'remarks', 'status', 'department_id').filter(code=scheduler).order_by('department_id')))
                    group_list = []
                    rownumber = 1
                    # print(dfmain)
                    for group in dfmain.itertuples():
                        # print(group.course)
                        table = {}
                        table['row'] = rownumber
                        table['scheduler'] = group.groupid
                        table['student'] = []

                        Students = filter(None,  group.students.split(","))
                        for stdgrp in Students:
                            StudentList = {
                                'scheduler': scheduler,
                                'stdgrp': stdgrp,
                                'name': str(stdgrp.split("-")[1])+'-'+getTableDepartment(stdgrp.split("-")[0], 'name'),
                            }
                            table['student'].append(StudentList)

                        table['coursecode'] = getCourseData(group.course, 'title').title()+'['+group.course+']' #.code +'-'+group.course.name
                        table['lecturer'] = '<i class="mdi mdi-alert-decagram-outline text-danger"></i>'
                        if group.lecturers != '':
                            table['lecturer'] = getCourseLecturer(str(group.lecturers), 'title').title()+' ('+group.lecturers.upper()+')'

                        table['day'] = getFullDay(group.lectureday)
                        table['starttime'] = formatTime(group.starttime)
                        table['endtime'] = formatTime(group.endtime)
                        table['venue'] = '<i class="mdi mdi-alert-decagram-outline text-danger"></i>'
                        if group.venue != None:
                            table['venue'] = getCourseVenue(group.venue, 'title').title()+' ('+group.venue.upper()+')'
                        table['remarks'] = getRemarks(group.remarks, group.status, group.venue)
                        table['link'] = 'scheduler='+scheduler+'&groupid='+group.groupid+'&studentgroup=ALL'
                        group_list.append(table)
                        rownumber += 1

                    context = {
                        'table_groups_scheduler': group_list,
                        'semesterRequire': Functions.getSemesterReq(),
                        'pagedata':{
                            'pageicon':'animation',
                            'pagetitle':'All Schedules',
                        }
                    }
                    return render(request, 'admin/generator/index.html', context)
            else:
                dfmain = pd.DataFrame(list(TablesGenerated.objects.values('groupid', 'totalenrol', 'starttime', 'endtime', 'lecturers', 'lectureday', 'venue', 'course', 'remarks', 'status', 'department_id').filter(code=scheduler, students__contains=studentgroup).order_by('students')))
                group_list = []
                rownumber = 1
                # tablesession = getTableData(scheduler)
                department = dfmain[['department_id']].iloc[0].department_id
                department = Functions.getDptName(studentgroup.split('-')[0]).upper()
                timetabletitle = ''+studentgroup.split("-")[1]+'-LEVEL '+department+' <br> '+getTableRegistry(scheduler, 'session')+' ['+getTableRegistry(scheduler, 'semestername')+' '+getSemester(studentgroup.split("-")[2])+' SEMESTER] TIMETABLE'
                for row in dfmain.itertuples():
                    table = {}
                    table['row'] = rownumber
                    table['coursecode'] = row.course
                    table['coursetitle'] = getCourseData(row.course, 'title').title()
                    table['day'] = getFullDay(row.lectureday)
                    table['start'] = formatTime(row.starttime)
                    table['end'] = formatTime(row.endtime)
                    table['lecturer'] = '<i class="mdi mdi-alert-decagram-outline text-danger"></i>'
                    if row.lecturers != '':
                        table['lecturer'] = getCourseLecturer(str(row.lecturers), 'title').title()+' ('+row.lecturers.upper()+')'
                    table['venue'] = '<i class="mdi mdi-alert-decagram-outline text-danger"></i>'
                    if row.venue != None:
                        table['venue'] = getCourseVenue(row.venue, 'title').title()+' ('+row.venue.upper()+')'
                    table['remark'] = getRemarks(row.remarks, row.status, row.venue)
                    table['link'] = 'scheduler='+scheduler+'&groupid='+row.groupid+'&studentgroup='+studentgroup

                    # table['semestertype'] = Functions.getSemesterName(table['semestertype'])
                    group_list.append(table)
                    rownumber += 1

                context = {
                    'table_groups_dpt_view': group_list,
                    'generationForm_1': True,
                    'viewgrouptabledata': 'True',
                    'timetabletitle':timetabletitle,
                    'semesterRequire': Functions.getSemesterReq(),
                    'pagedata':{
                        'pageicon':'timetable',
                        'pagetitle': studentgroup,
                    },
                    'modal':{
                        'modalicon': 'timetable',
                        'title': 'TIMETABLE: '+studentgroup,
                        'button': 'Create Scheduler',
                        'size': 'modal-lg'
                    }
                }
                return render(request, 'admin/generator/viewtimetable.html', context)
    else:
        return redirect('../login')


def newgenerator(request):
    if request.user.is_authenticated:
        form = generateForm()
        context = {
            'form': form,
            'generationForm': True,
            'semesterRequire': not(Functions.getSemesterReq()),
            'genFormDisplay': '',
            'submiturl':'addgenerator',
            'modal':{
                'modalicon': 'animation',
                'title': 'Create Scheduler',
                'button': 'Create Scheduler'
            }
        }
        return render(request, 'admin/includes/modalcontents/newfaculty.html', context)
    else:
        return redirect('../login')

@require_POST
def newgeneratoradd(request):
    if request.user.is_authenticated:
        session=request.POST.get("session", None)
        semestername=request.POST.get("semestername", None)
        semestertype=request.POST.get("semestertype", None)
        instance = ''
        form = ''
        try:
            if semestername != None and semestertype == None:
                instance = TableRegister.objects.get(session=session, semestername=semestername)
            else:
                instance = TableRegister.objects.get(session=session, semestertype=semestertype)
            form = generateForm(request.POST, instance=instance)
            if form.is_valid():
                result = '<div class="alert alert-danger col-12" role="alert" style="margin-bottom: 0;"><i class="mdi mdi-checkbox-marked-circle-outline"></i> A scheduler has already been created for the selected semester, please go to [Generate Schedule] to generate or view all timetables or change the selected semester and try again!</div>'
                return HttpResponse(result)
            else:
                return HttpResponse(str(form.errors))
        except TableRegister.DoesNotExist:
            form = generateForm(request.POST)
            if form.is_valid():
                data = form.cleaned_data
                instance = form.save()
                # genStat = Generator.startgen(data)
                result = '<div class="alert alert-success col-12" role="alert" style="margin-bottom: 0;"><i class="mdi mdi-checkbox-marked-circle-outline"></i> Table generated successfully!</div>'
                return HttpResponse(result)
            else:
                return HttpResponse(str(form.errors))
    else:
        return redirect('../login')


@require_GET
def openscheduler(request):
    if request.user.is_authenticated:
        id=request.GET.get("id", None)
        if id != None:
            instance = TableRegister.objects.get(code=id)
            form = generateForm(instance=instance)
            tableData = {
                'id': id,
                'gendate': getTableRegistry(id, 'gendate'),
                'semester': getTableRegistry(id, 'semestername'),
                'totalgen': getTableRegistry(id, 'totalgen'),
            }
            context = {
                'form': form,
                'tableData': tableData,
                'generationForm': True,
                'generationForm_1': True,
                'genFormDisplay': 'none',
                'genFormCardStyle':{
                    'modalbody': 'padding-bottom: 0;margin-bottom: -1px;',
                    'cardbody': 'padding-bottom: 0;',
                },
                'semesterRequire': not(Functions.getSemesterReq()),
                'submiturl':'startgeneration',
                'modal':{
                    'modalicon': 'animation',
                    'title': 'Generate Timetable',
                    'button': 'Generate Timetables',
                }
                }

            return render(request, 'admin/includes/modalcontents/newfaculty.html', context)

        #deleting record by id
        id=request.GET.get("delete", None)
        if id != None:
            instance = TableRegister.objects.get(code=id)
            instance.delete()
            result = '<div class="alert alert-success col-12" role="alert" style="margin-bottom: 0;"><i class="mdi mdi-checkbox-marked-circle-outline"></i> Scheduler: '+str(instance)+' deleted successfully!</div>'
            return HttpResponse(result)

    else:
       return redirect('../login')


@require_POST
def startgeneration(request):
    if request.user.is_authenticated:
        tableCode = request.POST.get("code", None)
        if tableCode != None:
            try:
                instance = TableRegister.objects.get(code=tableCode)
                form = generateForm(request.POST, instance=instance)
                # print(form)
                if form.is_valid():
                    data = form.cleaned_data
                    genStat = Generator.startgen(data, instance)
                    # result = '<div class="alert alert-success col-12" role="alert" style="margin-bottom: 0;"><i class="mdi mdi-checkbox-marked-circle-outline"></i> Scheduler is now generating your timetables, please wait...</div>'
                    return HttpResponse(genStat)
                else:
                    result = '<div class="alert alert-danger col-12" role="alert" style="margin-bottom: 0;"><i class="mdi mdi-checkbox-marked-circle-outline"></i> Invalid scheduler ID, please create a scheduler and try again!</div>'
                    return HttpResponse(result)
            except TableRegister.DoesNotExist:
                result = '<div class="alert alert-danger col-12" role="alert" style="margin-bottom: 0;"><i class="mdi mdi-checkbox-marked-circle-outline"></i> Invalid scheduler ID, please create a scheduler and try again!</div>'
                return HttpResponse(result)
        else:
            result = '<div class="alert alert-danger col-12" role="alert" style="margin-bottom: 0;"><i class="mdi mdi-checkbox-marked-circle-outline"></i> Invalid request, please reload and try again!</div>'
            return HttpResponse(result)


@require_GET
def manualscheduler(request):

    schedulerid=request.GET.get("scheduler", None)
    studentgroupid=request.GET.get("groupid", None)
    studentgroup=request.GET.get("studentgroup", None)
    print(schedulerid, ' - ', studentgroup)
    if schedulerid != None and studentgroup != None:
        instance = TablesGenerated.objects.get(groupid=studentgroupid)
        manualschedulerForm = manualSchedulerForm(instance=instance)
        result = '<div class="alert alert-danger col-12" role="alert" style="margin-bottom: 0;"><i class="mdi mdi-checkbox-marked-circle-outline"></i> Invalid request, please reload and try again!</div>'
        courseData = getCourseDataScheduler(studentgroupid)
        context = {
            'coursedata': courseData,
            'remarks': '',
            'generationForm_1': True,
            'generationForm': 'True',
            'backtablescheduler': schedulerid,
            'backtablestudents': studentgroup,
            'timetabletitle':studentgroupid,
            'semesterRequire': Functions.getSemesterReq(),
            'manualschedulerForm': manualschedulerForm,
            'matchesSugestion': ManualScheduler.getAvailableMatches(schedulerid, studentgroupid, instance.venue),
            'pagedata':{
                'pageicon':'timetable',
                # 'pagetitle': studentgroup,
            },
            'modal':{
                'modalicon': 'timetable',
                'title': 'TIMETABLE: ', #+studentgroup,
                'button': 'Create Scheduler',
                'size': 'modal-lg'
            }
        }
        return render(request, 'admin/generator/manualscheduler.html', context)
    else:
        result = '<div class="alert alert-danger col-12" role="alert" style="margin-bottom: 0;"><i class="mdi mdi-checkbox-marked-circle-outline"></i> Invalid request, make sure Course has been scheduled and try again!</div>'
        return HttpResponse(result)
