from django.db import models
from multiselectfield import MultiSelectField
from admin.models import Functions


DEPARTMENTS = Functions.getDepartmentList()
LECTURERS = Functions.getLecturerList()

class Course(models.Model):

    code = models.CharField(max_length=15,  unique=True)
    name = models.CharField(max_length=255)
    coursehourperweek = models.IntegerField(default=2)
    semester = models.IntegerField(default=0)
    subjecttype = models.IntegerField(default=0)
    departments = MultiSelectField(choices=DEPARTMENTS, max_length=2048)
    lecturers = MultiSelectField(choices=LECTURERS, max_length=2048)

    def __str__(self):
        return self.name

    def lecturer(self):
        return self.lecturers

    def contacthour(self):
        return self.coursehourperweek
