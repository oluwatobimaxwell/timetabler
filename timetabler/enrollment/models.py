from django.db import models
from courses_mgt.models import Course
from departments_mgt.models import Department

# Create your models here.
class Enrolment(models.Model):
    code = models.CharField(max_length=10,  unique=True)
    student_id = models.CharField(max_length=64, null=True)
    department = models.ForeignKey(Department, db_column='department', to_field='code', default=None, on_delete=models.CASCADE)
    course_code = models.ForeignKey(Course, db_column='course_code', to_field='code', default=None, on_delete=models.CASCADE)
    session = models.CharField(max_length=64, null=True)
    semesterName = models.CharField(max_length=64, blank=True)
    semesterType = models.IntegerField(default=0)
    level = models.IntegerField(default=0)

    # def __str__(self):
    #     enroldata = {
    #         'code': self.code,
    #         'department': self.department,
    #         'level': self.level,
    #         'course': self.course_code,
    #         'session': self.session,
    #         'semestername': self.semesterName,
    #         'semestertype': self.semesterType,
    #     }
    #     return enroldata
    #
    # def course_code(self):
    #     return self.course_code
    #
    # def student_id(self):
    #     return self.student_id
    #
    # def session(self):
    #     return self.session
    #
    # def semester(self):
    #     return self.semester
    #
    # def department(self):
    #     return self.department
    #
    # def level(self):
    #     return self.level
