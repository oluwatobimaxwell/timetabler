from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^updateSettings', views.UpdateConstraints, name='constraints_update'),
    url(r'^update', views.index, name='constraints'),
    # url(r'^addFaculty', views.newfacultyadd, name='add_faculty'),
    # url(r'^editFaculty', views.newfacultyedit, name='edit_faculty'),
    # url(r'^updateFaculty', views.updateFaculty, name='update_faculty'),
    # url(r'^mainRouter', views.mainRountingSystem, name='dataRouter'),
]
