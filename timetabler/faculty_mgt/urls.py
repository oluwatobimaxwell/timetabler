from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^faculties', views.index, name='faculty'),
    url(r'^newfaculty', views.newfaculty, name='new_faculty'),
    url(r'^addFaculty', views.newfacultyadd, name='add_faculty'),
    url(r'^editFaculty', views.newfacultyedit, name='edit_faculty'),
    url(r'^updateFaculty', views.updateFaculty, name='update_faculty'),
    url(r'^mainRouter', views.mainRountingSystem, name='dataRouter'),
]
