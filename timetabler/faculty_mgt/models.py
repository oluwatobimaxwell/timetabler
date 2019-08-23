from django.db import models
# from lecturers.models import Lecturers


# Create your models here.
class Faculty(models.Model):

    code = models.CharField(max_length=10,  unique=True)
    name = models.CharField(max_length=255,  unique=True)
    officer = models.CharField(max_length=10, null=True)
    image = models.ImageField(blank=True, null=True, upload_to="faculty_icons/%Y/%m/%D/")


    def __str__(self):
        return self.name

    def faculty_id(self):
        return self.code

    def faculty_officer(self):
        return self.officer
