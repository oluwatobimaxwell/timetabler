from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^lecturers', views.index, name='lecturers'),
    url(r'^newLecturer', views.newLecturer, name='new_Lecturer'),
    url(r'^addLecturer', views.newLectureradd, name='add_Lecturer'),
    url(r'^editLecturer', views.newLectureredit, name='edit_Lecturer'),
    url(r'^updateLecturer', views.updateLecturer, name='update_Lecturer'),
]
