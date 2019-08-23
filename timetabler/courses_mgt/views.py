from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import redirect
from .forms import newCourseForm
from django.views.decorators.http import require_POST, require_GET
from .models import Course
from admin.models import Functions
from faculty_mgt.models import Faculty
from departments_mgt.models import Department
from lecturers_mgt.models import Lecturers
import json

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        course_list = list(Course.objects.values())

        course_details = []
        rownumber = 1

        for cos_row in course_list:
            cos_row['row'] = rownumber
            # print(cos_row['officer'])
            cos_row['semester'] = Functions.getSemesterName(int(cos_row['semester']))
            cos_row['departments'] = len(cos_row['departments']) #Functions.StyleList(Functions, Department, cos_row['departments'])
            cos_row['lecturers'] = Functions.StyleList(Functions, Lecturers, cos_row['lecturers'])
            course_details.append(cos_row)
            rownumber += 1

        context = {
            'courses_list': course_details,
            'pagedata':{
                'pageicon':'text-subject',
                'pagetitle':'Courses Management',
            }
        }
        return render(request, 'admin/courses/index.html', context)
    else:
        return redirect('../login')



# NEW COURSE FORM
def newcourses(request):
    if request.user.is_authenticated:
        form = newCourseForm()
        context = {
            'form': form,
            'coursesForm': True,
            'semesterRequire': not(Functions.getSemesterReq()),
            'submiturl':'addcourses',
            'modal':{
                'modalicon': 'text-subject',
                'title': 'New Course',
                'button': 'Save Course',
            }
        }
        return render(request, 'admin/includes/modalcontents/newfaculty.html', context)
    else:
        return redirect('../login')


@require_POST
def newcoursesadd(request):
    if request.user.is_authenticated:
        form = newCourseForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            # print(form)
            instance = form.save()
            result = '<div class="alert alert-success col-12" role="alert"><i class="mdi mdi-checkbox-marked-circle-outline"></i>  New course: added successfully!</div>'
            return HttpResponse(result)
        else:
            return HttpResponse(str(form.errors))
    else:
        return redirect('../login')


# EDIT COURSE
@require_GET
def newcoursesedit(request):
    if request.user.is_authenticated:
        id=request.GET.get("id", None)
        if id != None:
            instance = Course.objects.get(id=id)
            form = newCourseForm(instance=instance)
            context = {
                'form': form,
                'submiturl':'updatecourses',
                'coursesForm':True,
                'semesterRequire': not(Functions.getSemesterReq()),
                'modal': {
                    'modalicon': 'text-subject',
                    'title': 'Update Course',
                    'button': 'Update Course',
                    'style': '',
                }
            }
            return render(request, 'admin/includes/modalcontents/newfaculty.html', context)

        #deleting record by id
        id=request.GET.get("delete", None)
        if id != None:
            instance = Course.objects.get(id=id)
            instance.delete()
            result = '<div class="alert alert-success col-12" role="alert"><i class="mdi mdi-checkbox-marked-circle-outline"></i> Course deleted successfully!</div>'
            return HttpResponse(result)

    else:
       return redirect('../login')


# COURSE UPDATE
@require_POST
def updatecourses(request):
    if request.user.is_authenticated:
        id=request.POST.get("code", None)
        courseName=request.POST.get("name", None)
        if id != None:
            instance = Course.objects.get(code=id)
            form = newCourseForm(request.POST,instance=instance )
            if form.is_valid():
                data = form.cleaned_data
                instance = form.save()
                result = '<div class="alert alert-success col-12" role="alert"><i class="mdi mdi-checkbox-marked-circle-outline"></i> '+courseName+' updated successfully!</div>'
                return HttpResponse(result)
            else:
                return HttpResponse(str(form.errors))
    else:
        return redirect('../login')
