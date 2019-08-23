from django.db import models
from faculty_mgt.models import Faculty
from departments_mgt.models import Department
from lecturers_mgt.models import Lecturers, staffTypes
from constraints.models import UserConstraints
from appsettings.models import appSettings
# from venues_mgt.models import Venue

# from courses_mgt.models import Course
import datetime
# Create your models here.
# class FacultySummary(Faculty):
#     class Meta:
#         proxy = True
#         verbose_name = ‘Sale Summary’
#         verbose_name_plural = ‘Sales Summary’


class Functions():
    def getFacultyList():
        all = Faculty.objects.all()
        params = []
        for item in all:
            params.append((item.code,item.name))
        return params

    def getLecturerList():
        all = Lecturers.objects.all()
        params = []
        for item in all:
            params.append((item.code,item.name))
        return params

    # def getVenueList():
    #     all = Venue.objects.all()
    #     params = []
    #     for item in all:
    #         params.append((item.code,item.name))
    #     return params

    def getDepartmentList():
        all = Department.objects.all()
        params = []
        for item in all:
            params.append((item.code,item.name))
        return params

    def getOfficersList():
        params = [
                    ('STF0000', 'Administrator'),
                    ('STF0001', 'Daniel Atunshe'),
                    ('STF0002', 'Mike Pence'),
                    ('STF0003', 'Stephen Atlah'),
                    ('STF0004', 'John King'),
                    ('STF0005', 'Benjamin Bells'),
                    ]
        return params

    def getNewId(AppModel, String, LeadZero):
        newid = String + str(LeadZero.format(1))
        if AppModel.objects.filter().count() > 0:
            newid = String + str(LeadZero.format(AppModel.objects.last().pk + 1))
        return newid

    def getSingleValueByCode(AppModel, QueryValue):
        return AppModel.objects.get(code=QueryValue).name

    def getMaxPriority():
        return 11

    def getWorkingDays():
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thurday', 'Friday', 'Saturday']
        times = ['Morning', 'Afternoon', 'Evening']
        periods = ['8:00 - 12:00','12:00 - 3:00','3:00 - 6:00']
        table = {
                'days': days,
                'times': times,
                'periods':zip(times, periods),
        }
        return table

    def getTotalDptInFac(AppModel, QueryValue):
        return AppModel.objects.filter(faculty=QueryValue).count()

    def getCourseTakenCount(AppModel, QueryValue):
        return AppModel.objects.filter(lecturers__contains=QueryValue).count()

    def subjectType():
        params = [
            ('0', 'Non-Practical Course'),
            ('1', 'Practical Course'),
            ('2', 'Field Event'),
        ]
        return params

    def getVenueTypes():
        params = [
                    ('0', 'Classroom'),
                    ('1', 'Lecture Hall'),
                    ('2', 'Laboratory'),
                    ('3', 'Clab'),
                    ]
        return params

    def getVenueName(type, venues):
        return venues[type][1]


    def getStudentLevels():
        return [(100,'100 Level'),
                  (200,'200 Level'),
                  (300,'300 Level'),
                  (400,'400 Level'),
                  (500,'500 Level')]

    def getSemestersList():
        return [(1,'First Semester'), (2,'Second Semester')]

    def getDaysAvailable():
        return [('mon', 'Mondays'),
                ('tue', 'Tuesdays'),
                ('wed', 'Wednesdays'),
                ('thu', 'Thurdays'),
                ('fri', 'Fridays'),
                ('sat', 'Saturday')]

    def getSemesterReq():
        # True means admission is Per Session Bases
        # False means admission is Per Semester Bases
        admissionType = appSettings.objects.get(id=1).admissionType
        return admissionType

    def getSettingsData(info):
        result = ''
        if info == 'semname':
            result = appSettings.objects.get(id=1).currentsemestername
        elif info == 'semtype':
            result = appSettings.objects.get(id=1).currentsemestertype
        elif info == 'session':
            result = appSettings.objects.get(id=1).currentsession
        elif info == 'adm':
            result = appSettings.objects.get(id=1).admissionType

        return result


    def getSemesterName(semester):
        if(semester == 0):
            return 'Both (1st & 2nd)'
        elif (semester == 1):
            return 'First'
        elif (semester == 2):
            return 'Second'
        else:
            return 'Unknown'

    def StyleList(self, model, items):
        if len(items) > 1:
            styled = '<ul class="numbered-bordered-list" style="padding: 0;">'
            for item in items:
                styled += '<li style="padding: 0; border: none">'+self.getSingleValueByCode(model, str(item))+'</li>'
            styled += '</ul>'
            return styled
        else:
            return items

    def getPreferredTiming():
        params = [  ('0', 'Morning'),
                    ('1', 'Afternoon'),
                    ('2', 'Evening'), ]
        return params

    def getLectConfirm(OPTIONS, Course):
        NewList = []
        for lecturer in OPTIONS:
            maxcontactHour = staffTypes.objects.get(type=lecturer['priorityNumber']).LecMaxCosPerSem
            courses = Course.objects.filter(lecturers__contains=lecturer['code'])
            currentHour = 0

            for course in courses:
                currentHour += course.coursehourperweek

            if(currentHour < maxcontactHour):
                NewList.append(lecturer)

        if len(NewList) <= 0:
            NewList.append({'code': 'No Lecturer Available', 'name': 'All lecturers are occupied!', 'priorityNumber': 0})
        print(NewList)
        return NewList

    # def getCheckLecNum(OPTIONS, Course):
    #     NewList = []
    #     maxCosPerLec = UserConstraints.lecSemesterMax(UserConstraints.objects.get(id=1))
    #     for lecturer in OPTIONS:
    #         count = Course.objects.filter(lecturers__contains=lecturer[0]).count()
    #         if(count < maxCosPerLec):
    #             NewList.append(lecturer)
    #     if len(NewList) <= 0:
    #         NewList.append(['No Lecturer Available','No free lecturer!'])
    #     return NewList

    def getSemesterAlias():
        current = datetime.datetime.now().strftime('%y')
        a = current+'A'
        b = current+'B'
        c = current+'C'
        return [(a, a),(b, b),(c, c)]

    def SessionList():
        now = datetime.datetime.now()
        current = int(now.year)
        session = []
        k = 0
        for x in range(5):
            session.append((''+str(current + 1 - k)+'/'+str(current - k)+'', ''+str(current + 1 - k)+'/'+str(current - k)+''))
            k += 1
        return session

    def AdmissionType():
        CHOICES=[(True,'Student enrolment is per SESSION'),
         (False,'Student enrolment is per SEMESTER')]
        return CHOICES

    def workTime():
        CHOICES = [
                    ('08:00', '08:00AM'),
                    ('09:00', '09:00AM'),
                    ('10:00', '10:00AM'),
                    ('11:00', '11:00AM'),
                    ('12:00', '12:00PM'),
                    ('13:00', '01:00PM'),
                    ('14:00', '02:00PM'),
                    ('15:00', '03:00PM'),
                    ('16:00', '04:00PM'),
                    ('17:00', '05:00PM'),
                    ('18:00', '06:00PM'),
                    ('19:00', '07:00PM'),
                    ('00:00', '-------'),
                    ]
        return CHOICES

    def getDptFac(QueryValue):
        return Department.objects.get(code=QueryValue).faculty

    def getDptName(QueryValue):
        return Department.objects.get(code=QueryValue).name
