from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import redirect
from .forms import newDepartmentForm
from django.views.decorators.http import require_POST, require_GET
from .models import Department
from admin.models import Functions
from faculty_mgt.models import Faculty
import json
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        department_list =  list(Department.objects.values())

        dpt_details = []
        rownumber = 1
        for dpt_row in department_list:
            dpt_row['row'] = rownumber
            dpt_row['facutly_name'] = Functions.getSingleValueByCode(Faculty, str(dpt_row['faculty_id']))
            dpt_row['officer'] = '-' #Functions.getSingleValueByCode(Faculty, str(dpt_row['officer']))
            dpt_details.append(dpt_row)
            rownumber += 1

        context = {
            'department_list': dpt_details,
            'idnum': 0,
            'pagedata':{
                'pageicon':'school',
                'pagetitle':'Departments Management',
            }
        }
        return render(request, 'admin/department/index.html', context)
    else:
        return redirect('../login')


def newdepartment(request):
    if request.user.is_authenticated:
        form = newDepartmentForm()
        context = {
            'form': form,
            'submiturl':'adddepartment',
            'modal':{
                'modalicon': 'school',
                'title': 'New Department',
                'button': 'Save Department',
            }
        }
        return render(request, 'admin/includes/modalcontents/newfaculty.html', context)
    else:
        return redirect('../login')


@require_POST
def newdepartmentadd(request):
    if request.user.is_authenticated:
        form = newDepartmentForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            instance = form.save(commit=False)
            instance = form.save()
            result = '<div class="alert alert-success col-12" role="alert"><i class="mdi mdi-checkbox-marked-circle-outline"></i> New department: '+str(instance)+' added successfully!</div>'
            return HttpResponse(result)
        else:
            return HttpResponse(str(form.errors))
    else:
        return redirect('../login')


@require_GET
def newdepartmentedit(request):
    if request.user.is_authenticated:
        id=request.GET.get("id", None)
        if id != None:
            instance = Department.objects.get(id=id)
            form = newDepartmentForm(instance=instance)
            context = {
             'form': form,
             'submiturl':'updateDepartment',
             'modal': {
                 'modalicon': 'school',
                 'title': 'Update Department',
                 'button': 'Update Department',
                 'style': '',
             }
            }
            return render(request, 'admin/includes/modalcontents/newfaculty.html', context)

        #deleting record by id
        id=request.GET.get("delete", None)
        if id != None:
            instance = Department.objects.get(id=id)
            instance.delete()
            result = '<div class="alert alert-success col-12" role="alert"><i class="mdi mdi-checkbox-marked-circle-outline"></i> Department: '+str(instance)+' deleted successfully!</div>'
            return HttpResponse(result)

    else:
        return redirect('../login')



@require_POST
def updateDepartment(request):
    if request.user.is_authenticated:
        id=request.POST.get("code", None)
        departmentName=request.POST.get("name", None)
        if id != None:
            instance = Department.objects.get(code=id)
            form = newDepartmentForm(request.POST,instance=instance )
            if form.is_valid():
                data = form.cleaned_data
                instance = form.save()
                result = '<div class="alert alert-success col-12" role="alert"><i class="mdi mdi-checkbox-marked-circle-outline"></i>Department of '+ departmentName +' updated successfully!</div>'
                return HttpResponse(result)
            else:
                return HttpResponse(str(form.errors))
    else:
        return redirect('../login')
