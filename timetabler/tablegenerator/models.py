from django.db import models
import datetime
from venues_mgt.models import Venue
from courses_mgt.models import Course
from departments_mgt.models import Department

# Create your models here.
class TableRegister(models.Model):
    code = models.CharField(unique=True, max_length=255, null=False)
    session = models.CharField(max_length=10, null=False)
    gendate = models.DateField((u"Date"), default=datetime.date.today)
    semestername = models.CharField(max_length=10, null=False)
    semestertype = models.IntegerField(default=1)
    totalgen = models.IntegerField(default=0)



class TablesGenerated(models.Model):
    code = models.ForeignKey(TableRegister, db_column='code', to_field='code',default=None, on_delete=models.CASCADE)
    groupid = models.CharField(unique=True, max_length=255, null=False)
    students = models.CharField(max_length=255, null=False)
    totalenrol = models.IntegerField(default=0)
    lectureday = models.CharField(max_length=3, null=False)
    starttime = models.TimeField((u"Conversation Time"), blank=False)
    endtime = models.TimeField((u"Conversation Time"), blank=False)
    course = models.ForeignKey(Course, db_column='course', to_field='code',default=None, on_delete=models.CASCADE)
    venue = models.ForeignKey(Venue, db_column='venue', null=True, to_field='code',default=None, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, db_column='department', null=True, to_field='code',default=None, on_delete=models.CASCADE)
    lecturers = models.CharField(max_length=2048)
    status = models.BooleanField(default=False)
    remarks = models.CharField(max_length=2048)
