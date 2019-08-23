from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^registrations', views.index, name='registrations'),
    url(r'^newRegistration', views.newRegistration, name='new_Registration'),
    url(r'^addRegistration', views.newRegistrationadd, name='add_Registration'),
    url(r'^editRegistration', views.newRegistrationedit, name='edit_Registration'),
    url(r'^updateRegistration', views.updateRegistration, name='update_Registration'),
    url(r'^BulkDataUpload', views.BulkDataUpload, name='BulkDataUpload'),
    url(r'^reacttest', views.reacttest, name='reacttest'),
]
