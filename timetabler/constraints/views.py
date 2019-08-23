from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf import settings
from django.shortcuts import redirect
from .forms import ConstraintsForm
from django.views.decorators.http import require_POST, require_GET
from .models import UserConstraints
from admin.models import Functions
from faculty_mgt.models import Faculty
from departments_mgt.models import Department
import json

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        form = ConstraintsForm(instance=UserConstraints.objects.get(id=1))
        context = {
            'form': form,
            'pagedata':{
                'pageicon':'chart-bar-stacked',
                'pagetitle':'Timetable Constraints',
            }
        }
        return render(request, 'admin/constraints/index.html', context)
    else:
        return redirect('../login')


@require_POST
def UpdateConstraints(request):
    if request.user.is_authenticated:
        form = ConstraintsForm(request.POST, instance=UserConstraints.objects.get(id=1))
        if form.is_valid():
            data = form.cleaned_data
            constraint = form.save()
            result = '<div class="alert alert-success col-12" role="alert"><i class="mdi mdi-checkbox-marked-circle-outline"></i>  Constraints have been successfully updated!</div>'
            return HttpResponse(result)
        else:
            return HttpResponse(str(form.errors))
    else:
        return redirect('../login')
