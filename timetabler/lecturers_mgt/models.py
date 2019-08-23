from django.db import models
from faculty_mgt.models import Faculty
from departments_mgt.models import Department



class staffTypes(models.Model):
    type = models.IntegerField(default=1, unique=True)
    designation = models.CharField(max_length=255, null=True, unique=True)
    LecMaxCosPerSem = models.IntegerField(default=10)
    LecMaxCosPerDay = models.IntegerField(default=2)

    def __str__(self):
        return self.designation

class Lecturers(models.Model):

    code = models.CharField(unique=True, max_length=10, null=False)
    name  = models.CharField(max_length=255, null=True)
    facultyLec = models.ForeignKey(Faculty, db_column='facultyLec', to_field='code', default=None, on_delete=models.CASCADE)
    departmentLec = models.ForeignKey(Department, db_column='departmentLec', to_field='code', default=None, on_delete=models.CASCADE)
    priorityNumber  = models.ForeignKey(staffTypes, db_column='priorityNumber', to_field='type', default=None, on_delete=models.CASCADE)
    visiting = models.BooleanField(default=False)

    mon = models.BooleanField(default=True)
    tue = models.BooleanField(default=True)
    wed = models.BooleanField(default=True)
    thu = models.BooleanField(default=True)
    fri = models.BooleanField(default=True)
    sat = models.BooleanField(default=False)

    monFrom = models.TimeField((u"Conversation Time"), blank=False, default='08:00')
    monTo = models.TimeField((u"Conversation Time"), blank=False, default='18:00')
    tueFrom = models.TimeField((u"Conversation Time"), blank=False, default='08:00')
    tueTo = models.TimeField((u"Conversation Time"), blank=False, default='18:00')
    wedFrom = models.TimeField((u"Conversation Time"), blank=False, default='08:00')
    wedTo = models.TimeField((u"Conversation Time"), blank=False, default='18:00')
    thuFrom = models.TimeField((u"Conversation Time"), blank=False, default='08:00')
    thuTo = models.TimeField((u"Conversation Time"), blank=False, default='18:00')
    friFrom = models.TimeField((u"Conversation Time"), blank=False, default='08:00')
    friTo = models.TimeField((u"Conversation Time"), blank=False, default='18:00')
    satFrom = models.TimeField((u"Conversation Time"), blank=False, default='00:00')
    satTo = models.TimeField((u"Conversation Time"), blank=False, default='00:00')
