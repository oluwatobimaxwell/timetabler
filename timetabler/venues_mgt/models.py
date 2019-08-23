from django.db import models
from multiselectfield import MultiSelectField
from admin.models import Functions
# Create your models here.
LEVELS = Functions.getStudentLevels()
DAYS = Functions.getDaysAvailable()
FACULTIES = Functions.getFacultyList()
DEPARTMENTS = Functions.getDepartmentList()

class Venue(models.Model):

    code = models.CharField(max_length=10,  unique=True)
    name = models.CharField(max_length=10,  unique=True)
    capacity = models.IntegerField(default=50)
    type = models.IntegerField(default=0)
    reservedFaculty = MultiSelectField(choices=FACULTIES,  max_length=2048)
    reservedDepartment = MultiSelectField(choices=DEPARTMENTS,  max_length=2048)
    reservedLevel = MultiSelectField(choices=LEVELS,  max_length=2048)
    reservedDays = MultiSelectField(choices=DAYS,  max_length=2048)
