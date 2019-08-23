from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^appsettings', views.index, name='appsettings'),
    url(r'^updateSettings', views.UpdateAppSettings, name='settings_update'),
    url(r'^lecturerRoles', views.lecturerRoles, name='lecturerRoles'),
    url(r'^new_lecturer_type', views.new_lecturer_type, name='new_lecturer_type'),
    # url(r'^addFaculty', views.newfacultyadd, name='add_faculty'),
    url(r'^editLecturerType', views.editLecturerType, name='editLecturerType'),
    # url(r'^updateFaculty', views.updateFaculty, name='update_faculty'),
    # url(r'^mainRouter', views.mainRountingSystem, name='dataRouter'),
]
