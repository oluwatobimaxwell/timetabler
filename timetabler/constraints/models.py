from django.db import models


class UserConstraints(models.Model):

    LectureStartTime = models.TimeField((u"Conversation Time"), blank=False)
    LectureCloseTime = models.TimeField((u"Conversation Time"), blank=False)
    AllowDailyBrkTime = models.BooleanField(default=True)
    DailyBrkStartTime = models.TimeField((u"Conversation Time"), blank=False)
    DailyBrkDuration = models.IntegerField(default=30)
    MuslimWeekPrayer = models.BooleanField(default=True)
    MuslimPrayStart = models.TimeField((u"Conversation Time"), blank=False)
    MuslimPrayDuration = models.IntegerField(default=60)
    LecMaxCosPerSem = models.IntegerField(default=3)
    LecMaxClassPerDay = models.IntegerField(default=2)
    LecMinBtwClasses = models.IntegerField(default=30)
    StuMaxClassPerDay = models.IntegerField(default=2)
    StuMinBtwClasses = models.IntegerField(default=30)
    visitingLecturer = models.BooleanField(default=True)
    restrictVisiting = models.BooleanField(default=True)
    AssignSaturdays = models.BooleanField(default=False)

    def start(self):
        return self.LectureStartTime

    def close(self):
        return self.LectureCloseTime

    def allowBrk(self):
        return self.AllowDailyBrkTime

    def breakLength(self):
        return self.DailyBrkStartTime

    def prayer(self):
        return self.MuslimWeekPrayer

    def prayerStart(self):
        return self.MuslimPrayStart

    def prayerLength(self):
        return self.MuslimPrayDuration

    def lecSemesterMax(self):
        return self.LecMaxCosPerSem

    def lecMaxClass(self):
        return self.LecMaxClassPerDay

    def lecminBtw(self):
        return self.LecMinBtwClasses

    def stumaxClass(self):
        return self.StuMaxClassPerDay

    def stuminBtw(self):
        return self.StuMinBtwClasses

    def visiting(self):
        return self.visitingLecturer


    def has_add_permission(self, *args, **kwargs):
        return not UserConstraints.objects.exists()
