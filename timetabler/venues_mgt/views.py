from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import redirect
from .forms import newVenueForm
from django.views.decorators.http import require_POST, require_GET
from .models import Venue
from admin.models import Functions
# from faculty_mgt.models import Faculty
import json
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        Venue_list = list(Venue.objects.values())
        venue_details = []
        rownumber = 1
        for ven in Venue_list:
            ven['row'] = rownumber
            venType = Functions.getVenueName(ven['type'], Functions.getVenueTypes())
            if ven['type'] == 0:
                ven['type'] = '<label class="badge badge-danger">'+venType+'</label>'
            elif ven['type'] == 1:
                ven['type'] = '<label class="badge badge-success">'+venType+'</label>'
            elif ven['type'] == 2:
                ven['type'] = '<label class="badge badge-warning">'+venType+'</label>'
            elif ven['type'] == 3:
                ven['type'] = '<label class="badge badge-info">'+venType+'</label>'

            venue_details.append(ven)
            ven['row']
            rownumber += 1

        context = {
            'venue_list': venue_details,
            'idnum': 0,
            'pagedata':{
                'pageicon':'fireplace-off',
                'pagetitle':'Venues Management',
            }
        }
        return render(request, 'admin/venues/index.html', context)
    else:
        return redirect('../login')

def newVenue(request):
    if request.user.is_authenticated:
        form = newVenueForm()
        context = {
            'form': form,
            'venueForm': True,
            'submiturl':'addvenue',
            'modal':{
                'modalicon': 'fireplace-off',
                'title': 'New Venue',
                'button': 'Save Venue',
            }
        }
        return render(request, 'admin/includes/modalcontents/newfaculty.html', context)
    else:
        return redirect('../login')


@require_POST
def newVenueadd(request):
    if request.user.is_authenticated:
        form = newVenueForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # print(form)
            new_faculty = form.save()
            result = '<div class="alert alert-success col-12" role="alert"><i class="mdi mdi-checkbox-marked-circle-outline"></i>  New venue added successfully!</div>'
            return HttpResponse(result)
        else:
            return HttpResponse(str(form.errors))
    else:
        return redirect('../login')

# EDIT VENUE
@require_GET
def newVenueedit(request):
    if request.user.is_authenticated:
        id=request.GET.get("id", None)
        if id != None:
            instance = Venue.objects.get(id=id)
            form = newVenueForm(instance=instance)
            context = {
                'form': form,
                'venueForm': True,
                'submiturl':'updatevenue',
                'modal': {
                    'modalicon': 'fireplace-off',
                    'title': 'Update Venue',
                    'button': 'Update Venue',
                    'style': '',
                }
            }
            return render(request, 'admin/includes/modalcontents/newfaculty.html', context)

        #deleting record by id
        id=request.GET.get("delete", None)
        if id != None:
            instance = Venue.objects.get(id=id)
            instance.delete()
            result = '<div class="alert alert-success col-12" role="alert"><i class="mdi mdi-checkbox-marked-circle-outline"></i> Venue deleted successfully!</div>'
            return HttpResponse(result)

    else:
       return redirect('../login')


# UPDATE VENUE
@require_POST
def updateVenue(request):
    result = {}
    if request.user.is_authenticated:
        id=request.POST.get("code", None)
        venueName=request.POST.get("name", None)
        if id != None:
            instance = Venue.objects.get(code=id)
            form = newVenueForm(request.POST,instance=instance )
            if form.is_valid():
                data = form.cleaned_data
                new_faculty = form.save()
                result = '<div class="alert alert-success col-12" role="alert"><i class="mdi mdi-checkbox-marked-circle-outline"></i>Venue '+ venueName +' updated successfully!</div>'
                return HttpResponse(result)
            else:
                return HttpResponse(str(form.errors))
    else:
        return redirect('../login')
