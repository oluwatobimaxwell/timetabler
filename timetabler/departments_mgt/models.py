from django.db import models
# from lecturers.models import Lecturers
from faculty_mgt.models import Faculty

# Create your models here.
class Department(models.Model):

    code = models.CharField(max_length=10,  unique=True)
    name = models.CharField(max_length=255,  unique=True)
    faculty = models.ForeignKey(Faculty, db_column='faculty', to_field='code',default=None, on_delete=models.CASCADE)
    officer = models.CharField(max_length=10, null=True)

    def __str__(self):
        return self.name

    def department_id(self):
        return self.code

    def dept_faculty_id(self):
        return self.faculty

    def department_officer(self):
        return self.officer
