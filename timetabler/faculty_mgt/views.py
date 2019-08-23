from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import redirect
from .forms import newFacultyForm
from django.views.decorators.http import require_POST, require_GET
from .models import Faculty
from lecturers_mgt.models import Lecturers
from departments_mgt.models import Department
from admin.models import Functions
from courses_mgt.models import Course
import json

# FACULTY INDEX
def index(request):
    if request.user.is_authenticated:
        faculty_list = list(Faculty.objects.values())

        fac_details = []
        rownumber = 1

        for fac_row in faculty_list:
            fac_row['row'] = rownumber
            print(fac_row['officer'])
            fac_row['officer'] = fac_row['officer']#Functions.getSingleValueByCode(Lecturers, str(fac_row['officer']))
            fac_row['totaldpt'] = Functions.getTotalDptInFac(Department, str(fac_row['code']))
            fac_details.append(fac_row)
            rownumber += 1

        context = {
            'faculty_list': fac_details,
            'pagedata':{
                'pageicon':'domain',
                'pagetitle':'Faculties Management',
            }
        }
        return render(request, 'admin/faculty/index.html', context)
    else:
        return redirect('../login')

# FACULT NEW FORM
def newfaculty(request):
    if request.user.is_authenticated:
        form = newFacultyForm()
        context = {
            'form': form,
            'facultyForm': True,
            'submiturl':'addFaculty',
            'modal':{
                'modalicon': 'domain',
                'title': 'New Faculty',
                'button': 'Save Faculty',
            }
        }
        return render(request, 'admin/includes/modalcontents/newfaculty.html', context)
    else:
        return redirect('../login')

# SAVE NEW FACULTY
@require_POST
def newfacultyadd(request):
    if request.user.is_authenticated:
        form = newFacultyForm(request.POST, request.FILES)
        if form.is_valid():
            data = form.cleaned_data
            new_faculty = form.save()
            result = '<div class="alert alert-success col-12" role="alert"><i class="mdi mdi-checkbox-marked-circle-outline"></i> New faculty: '+str(new_faculty)+' added successfully!</div>'
            return HttpResponse(result)
        else:
            return HttpResponse(str(form.errors))
    else:
        return redirect('../login')


#EDIT FACULTY
@require_GET
def newfacultyedit(request):
    if request.user.is_authenticated:
        id=request.GET.get("id", None)
        if id != None:
            instance = Faculty.objects.get(id=id)
            form = newFacultyForm(instance=instance)
            context = {
                'form': form,
                'submiturl':'updateFaculty',
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
            instance = Faculty.objects.get(id=id)
            instance.delete()
            result = '<div class="alert alert-success col-12" role="alert"><i class="mdi mdi-checkbox-marked-circle-outline"></i> Faculty: '+str(instance)+' deleted successfully!</div>'
            return HttpResponse(result)

    else:
       return redirect('../login')



# UPDATE EXISTING FACULTY
@require_POST
def updateFaculty(request):
    if request.user.is_authenticated:
        id=request.POST.get("code", None)
        facultyName=request.POST.get("name", None)
        if id != None:
            instance = Faculty.objects.get(code=id)
            form = newFacultyForm(request.POST, request.FILES, instance=instance)
            if form.is_valid():
                data = form.cleaned_data
                new_faculty = form.save()
                result = '<div class="alert alert-success col-12" role="alert"><i class="mdi mdi-checkbox-marked-circle-outline"></i> '+facultyName+' updated successfully!</div>'
                return HttpResponse(result)
            else:
                return HttpResponse(str(form.errors))
    else:
        return redirect('../login')



# MAIN GET ROUTER API
@require_GET
def mainRountingSystem(request):
    if request.user.is_authenticated:
        source =request.GET.get("source", None)
        value = (request.GET.get("value", None)).split(",")
        target = request.GET.get("target", None)
        type = request.GET.get("type", None)
        if source != None:
            typeInpu = ''
            if int(type) == 0:
                typeInpu = 'multiple="multiple"'

            listOutput = '<select name="'+target+'" class="form-control p-input" '+typeInpu+' id="id_'+target+'">'

            for code in value:
                CHOICES = []
                if source == 'faculty':
                    CHOICES = Department.objects.filter(faculty=code).values("code","name")
                elif source == 'department':
                    # FURTHER TO FILTER FOR LECTURERS WITH LESS THAN MAXIMUM COURSES
                    OPTIONS = Lecturers.objects.filter(departmentLec=code).values("code","name","priorityNumber")
                    CHOICES = Functions.getLectConfirm(OPTIONS, Course)

                for option in CHOICES:
                    listOutput += '<option value="'+option['code']+'">'+option['name']+'</option>'

            listOutput += '</select>'
            return HttpResponse(listOutput)


    else:
        return redirect('../login')
