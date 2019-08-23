from django.db import models


class Lecturers(models.Model):

    code = models.CharField(unique=True, max_length=10, null=False)
    name  = models.CharField(max_length=255, null=True)
    facultyLec = models.CharField(max_length=255, null=True)
    departmentLec = models.CharField(max_length=255, null=True)
    priorityNumber  = models.IntegerField(default=1)
    mon_0 = models.BooleanField(default=True)
    mon_1 = models.BooleanField(default=True)
    mon_2 = models.BooleanField(default=True)
    tue_0 = models.BooleanField(default=True)
    tue_1 = models.BooleanField(default=True)
    tue_2 = models.BooleanField(default=True)
    wed_0 = models.BooleanField(default=True)
    wed_1 = models.BooleanField(default=True)
    wed_2 = models.BooleanField(default=True)
    thu_0 = models.BooleanField(default=True)
    thu_1 = models.BooleanField(default=True)
    thu_2 = models.BooleanField(default=True)
    fri_0 = models.BooleanField(default=True)
    fri_1 = models.BooleanField(default=True)
    fri_2 = models.BooleanField(default=True)
    sat_0 = models.BooleanField(default=False)
    sat_1 = models.BooleanField(default=False)
    sat_2 = models.BooleanField(default=False)
