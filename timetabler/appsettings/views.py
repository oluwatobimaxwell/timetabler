from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import redirect
from .forms import AppSettingsForm
from django.views.decorators.http import require_POST, require_GET
from .models import appSettings
from admin.models import Functions
from faculty_mgt.models import Faculty
from departments_mgt.models import Department
from lecturers_mgt.forms import newLectuerType
from lecturers_mgt.models import staffTypes
import json

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        form = AppSettingsForm(instance=appSettings.objects.get(id=1))
        appLecturer = list(staffTypes.objects.values())
        context = {
            'form': form,
            'appLecturer': appLecturer,
            'semesterRequire': Functions.getSemesterReq(),
            'pagedata':{
                'pageicon':'settings-outline',
                'pagetitle':'Other Settings',
            }
        }
        return render(request, 'admin/appsettings/index.html', context)
    else:
        return redirect('../login')


@require_POST
def UpdateAppSettings(request):
    if request.user.is_authenticated:
        form = AppSettingsForm(request.POST, instance=appSettings.objects.get(id=1))
        if form.is_valid():
            data = form.cleaned_data
            constraint = form.save()
            result = '<div class="alert alert-success col-12" role="alert"><i class="mdi mdi-checkbox-marked-circle-outline"></i>  Settings have been successfully updated!</div>'
            return HttpResponse(result)
        else:
            return HttpResponse(str(form.errors))
    else:
        return redirect('../login')


@require_POST
def lecturerRoles(request):
    if request.user.is_authenticated:
        form = newLectuerType(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            constraint = form.save()
            result = '<div class="alert alert-success col-12" role="alert"><i class="mdi mdi-checkbox-marked-circle-outline"></i>  New type of lectuer added successfully!</div>'
            return HttpResponse(result)
        else:
            form = newLectuerType(request.POST, instance = staffTypes.objects.get(type=request.POST.get("type", None)))
            if form.is_valid():
                data = form.cleaned_data
                constraint = form.save()
                result = '<div class="alert alert-success col-12" role="alert"><i class="mdi mdi-checkbox-marked-circle-outline"></i>  Lectuer type updated successfully!</div>'
                return HttpResponse(result)
            else:
                return HttpResponse(str(form.errors))
    else:
        return redirect('../login')


def new_lecturer_type(request):
    if request.user.is_authenticated:
        form = newLectuerType()
        context = {
            'form': form,
            'facultyForm': True,
            'submiturl':'lecturerRoles',
            'modal':{
                'modalicon': 'teach',
                'title': 'New Lectuer Type',
                'button': 'Save Lecturer Type',
            }
        }
        return render(request, 'admin/includes/modalcontents/newfaculty.html', context)
    else:
        return redirect('../login')


@require_GET
def editLecturerType(request):
    if request.user.is_authenticated:
        id=request.GET.get("id", None)
        if id != None:
            instance = staffTypes.objects.get(id=id)
            form = newLectuerType(instance=instance)
            context = {
                'form': form,
                'submiturl':'lecturerRoles',
                'modal': {
                    'modalicon': 'domain',
                    'title': 'Update Faculty',
                    'button': 'Update Faculty',
                    'style': '',
                }
            }
            return render(request, 'admin/includes/modalcontents/newfaculty.html', context)

        #deleting record by id
        id=request.GET.get("delete", None)
        if id != None:
            instance = staffTypes.objects.get(id=id)
            instance.delete()
            result = '<div class="alert alert-success col-12" role="alert"><i class="mdi mdi-checkbox-marked-circle-outline"></i> Lecturer Type: '+str(instance)+' deleted successfully!</div>'
            return HttpResponse(result)

    else:
       return redirect('../login')
