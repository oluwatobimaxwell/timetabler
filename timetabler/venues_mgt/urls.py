from django.conf.urls import url, include
from . import views

urlpatterns = [
    url(r'^venues', views.index, name='venue'),
    url(r'^newvenue', views.newVenue, name='new_venue'),
    url(r'^addvenue', views.newVenueadd, name='add_enue'),
    url(r'^editvenue', views.newVenueedit, name='edit_venue'),
    url(r'^updatevenue', views.updateVenue, name='update_venue'),
]
