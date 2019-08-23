from django.db import models


class appSettings(models.Model):

    admissionType = models.BooleanField(default=True)
    currentsession = models.CharField(max_length=64)
    currentsemestername = models.CharField(max_length=64, blank=True, null=True)
    currentsemestertype = models.IntegerField(default=1)

    def issessional(self):
        return self.admissionType

    def thissession(self):
        return self.currentsession

    def thissemestername(self):
        return self.currentsemestername

    def thissemestertype(self):
        return self.currentsemestertype

    def has_add_permission(self, *args, **kwargs):
        return not UserConstraints.objects.exists()
