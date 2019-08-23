from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import redirect
from .forms import newLecturerForm
from django.views.decorators.http import require_POST, require_GET
from .models import Lecturers, staffTypes
from admin.models import Functions
from faculty_mgt.models import Faculty
from departments_mgt.models import Department
from courses_mgt.models import Course
from constraints.models import UserConstraints
from tablegenerator.genprocessor import constraints as constraintsValues
import json

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        Lecturers_list =  list(Lecturers.objects.values())
        lec_details = []
        rownumber = 1
        for lec_row in Lecturers_list:
            lec_row['row'] = rownumber
            lec_row['facultyLec'] = Functions.getSingleValueByCode(Faculty, str(lec_row['facultyLec_id']))
            lec_row['departmentLec'] = Functions.getSingleValueByCode(Department, str(lec_row['departmentLec_id']))
            lec_row['cousesTaken'] = Functions.getCourseTakenCount(Course, str(lec_row['code']))
            lec_row['priorityNumber'] = lec_row['priorityNumber_id'] #staffTypes.objects.get(id=lec_row['priorityNumber_id']).type
            lec_details.append(lec_row)
            rownumber += 1

        context = {
            'lecturers': Lecturers_list,
            'maximumpriority': Functions.getMaxPriority() - 1,
            'pagedata':{
                'pageicon':'teach',
                'pagetitle':'Lecturers Management',
            }
        }
        return render(request, 'admin/lecturer/index.html', context)
    else:
        return redirect('../login')

# NEW LECTURER FORM
def newLecturer(request):
        if request.user.is_authenticated:
            form = newLecturerForm()
            tabler = Functions.getWorkingDays()
            visitingCheck = UserConstraints.objects.get(id=1).visiting
            context = {
                'form': form,
                'visiting': visitingCheck,
                'lecturerForm': True,
                'Available': tabler,
                'Saturday': constraintsValues('AssignSaturdays'),
                'submiturl':'addLecturer',
                'modal':{
                    'modalicon': 'teach',
                    'title': 'New Lecturer',
                    'button': 'Save Lecturer',
                }
            }
            return render(request, 'admin/includes/modalcontents/newfaculty.html', context)
        else:
            return redirect('../login')


# SAVE NEW LECTURE
@require_POST
def newLectureradd(request):
    if request.user.is_authenticated:
        form = newLecturerForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            instance = form.save()
            print(data)
            result = '<div class="alert alert-success col-12" role="alert">New lecturer: added successfully!</div>'
            return HttpResponse(result)
        else:
            return HttpResponse(str(form.errors))
    else:
        return redirect('../login')


# EDIT LECTURER
@require_GET
def newLectureredit(request):
    if request.user.is_authenticated:
        id=request.GET.get("id", None)
        if id != None:
            instance = Lecturers.objects.get(id=id)
            form = newLecturerForm(instance=instance)
            tabler = Functions.getWorkingDays()
            visitingCheck = UserConstraints.objects.get(id=1).visiting
            context = {
                'form': form,
                'lecturerForm': True,
                'visiting': visitingCheck,
                'Saturday': constraintsValues('AssignSaturdays'),
                'Available': tabler,
                'submiturl':'updateLecturer',
                'modal': {
                    'modalicon': 'teach',
                    'title': 'Update Lecturer',
                    'button': 'Update Lecturer',
                    'style': '',
                }
            }
            return render(request, 'admin/includes/modalcontents/newfaculty.html', context)

        #deleting record by id
        id=request.GET.get("delete", None)
        if id != None:
            instance = Lecturers.objects.get(id=id)
            instance.delete()
            result = '<div class="alert alert-success col-12" role="alert"><i class="mdi mdi-checkbox-marked-circle-outline"></i> Lecturer: deleted successfully!</div>'
            return HttpResponse(result)

    else:
       return redirect('../login')



# UPDATE EXISTING LECTURER
@require_POST
def updateLecturer(request):
    if request.user.is_authenticated:
        id=request.POST.get("code", None)
        if id != None:
            instance = Lecturers.objects.get(code=id)
            form = newLecturerForm(request.POST,instance=instance )
            if form.is_valid():
                data = form.cleaned_data
                instance = form.save()
                result = '<div class="alert alert-success col-12" role="alert"><i class="mdi mdi-checkbox-marked-circle-outline"></i>Lecturer updated successfully!</div>'
                return HttpResponse(result)
            else:
                return HttpResponse(str(form.errors))
    else:
        return redirect('../login')
