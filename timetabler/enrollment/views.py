from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import redirect
from .forms import EnrolmentForm, BulkDataUpload
from django.views.decorators.http import require_POST, require_GET
from .models import Enrolment
from admin.models import Functions
from departments_mgt.models import Department
from courses_mgt.models import Course
# from faculty_mgt.models import Faculty
import json

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        reg_list = list(Enrolment.objects.values())
        reg_details = []
        rownumber = 1
        for reg in reg_list:
            reg['row'] = rownumber
            reg['course_code'] = Functions.getSingleValueByCode(Course, reg['course_code_id'])
            reg['department'] = Functions.getSingleValueByCode(Department, reg['department_id'])
            reg['semesterType'] = Functions.getSemesterName(reg['semesterType'])
            reg_details.append(reg)
            rownumber += 1


        context = {
            'reg_details': reg_details,
            'idnum': 0,
            'pagedata':{
                'pageicon':'table-row-plus-before',
                'pagetitle':'Student Enrolments',
            }
        }
        return render(request, 'admin/registration/index.html', context)
    else:
        return redirect('../login')


def newRegistration(request):
    if request.user.is_authenticated:
        form = EnrolmentForm()
        context = {
            'form': form,
            'registrationForm': True,
            'semesterRequire': Functions.getSemesterReq(),
            'submiturl':'addRegistration',
            'modal':{
                'modalicon': 'table-row-plus-before',
                'title': 'New Course Registration',
                'button': 'Save Registration',
            }
        }
        return render(request, 'admin/includes/modalcontents/newfaculty.html', context)
    else:
        return redirect('../login')


def BulkDataUpload(request):
    if request.user.is_authenticated:
        form = BulkDataUpload()
        context = {
            'form': form,
            'submiturl':'addRegistration',
            'modal':{
                'modalicon': 'database-import',
                'title': 'Upload Enrolment Data',
                'button': 'Upload Now',
            }
        }
        return render(request, 'admin/includes/modalcontents/newfaculty.html', context)
    else:
        return redirect('../login')




@require_POST
def newRegistrationadd(request):
    if request.user.is_authenticated:
        form = EnrolmentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            instance = form.save()
            result = '<div class="alert alert-success col-12" role="alert"><i class="mdi mdi-checkbox-marked-circle-outline"></i>  New course registration added successfully!</div>'
            return HttpResponse(result)
        else:
            return HttpResponse(str(form.errors))
    else:
        return redirect('../login')



# EDIT COURSE
@require_GET
def newRegistrationedit(request):
    if request.user.is_authenticated:
        id=request.GET.get("id", None)
        if id != None:
            instance = Enrolment.objects.get(id=id)
            form = EnrolmentForm(instance=instance)
            context = {
                'form': form,
                'submiturl':'updateRegistration',
                'registrationForm':True,
                'modal': {
                    'modalicon': 'text-subject',
                    'title': 'Update Registration',
                    'button': 'Update Registration',
                    'style': '',
                }
            }
            return render(request, 'admin/includes/modalcontents/newfaculty.html', context)

        #deleting record by id
        id=request.GET.get("delete", None)
        if id != None:
            instance = Enrolment.objects.get(id=id)
            instance.delete()
            result = '<div class="alert alert-success col-12" role="alert"><i class="mdi mdi-checkbox-marked-circle-outline"></i> Registration deleted successfully!</div>'
            return HttpResponse(result)

    else:
       return redirect('../login')


# COURSE UPDATE
@require_POST
def updateRegistration(request):
    if request.user.is_authenticated:
        id=request.POST.get("code", None)
        courseName=request.POST.get("student_id", None)
        if id != None:
            instance = Enrolment.objects.get(code=id)
            form = EnrolmentForm(request.POST,instance=instance )
            if form.is_valid():
                data = form.cleaned_data
                instance = form.save()
                result = '<div class="alert alert-success col-12" role="alert"><i class="mdi mdi-checkbox-marked-circle-outline"></i> '+courseName+' updated successfully!</div>'
                return HttpResponse(result)
            else:
                return HttpResponse(str(form.errors))
    else:
        return redirect('../login')


def reacttest(request):
    if request.user.is_authenticated:
        response = {
            "status": True,
            "username":"Oluwatobi Maxwellium",
            "counters": [{"id":1,"value":56},{"id":2,"value":24},{"id":3,"value":32},{"id":4,"value":27},{"id":5,"value":37}],
        }
        return HttpResponse(
                json.dumps(response)
                # content_type = 'application/javascript; charset=utf8'
                )
    else:
        response = {
            "status": False
        }
        return HttpResponse(
                json.dumps(response),
                content_type = 'application/javascript; charset=utf8'
                )
