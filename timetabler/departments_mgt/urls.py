from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^departments', views.index, name='department'),
    url(r'^newdepartment', views.newdepartment, name='new_department'),
    url(r'^adddepartment', views.newdepartmentadd, name='add_department'),
    url(r'^editdepartment', views.newdepartmentedit, name='edit_department'),
    url(r'^updateDepartment', views.updateDepartment, name='update_Department'),
]
