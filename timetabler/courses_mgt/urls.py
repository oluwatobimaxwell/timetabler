from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^courses', views.index, name='courses'),
    url(r'^newcourses', views.newcourses, name='new_courses'),
    url(r'^addcourses', views.newcoursesadd, name='add_courses'),
    url(r'^editcourses', views.newcoursesedit, name='edit_courses'),
    url(r'^updatecourses', views.updatecourses, name='update_courses'),
]
