from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^generator', views.index, name='generator'),
    url(r'^newgenerator', views.newgenerator, name='new_generator'),
    url(r'^addgenerator', views.newgeneratoradd, name='add_generator'),
    url(r'^openscheduler', views.openscheduler, name='openscheduler'),
    url(r'^startgeneration', views.startgeneration, name='startgeneration'),
    url(r'^manualscheduler', views.manualscheduler, name='manualscheduler'),
]
