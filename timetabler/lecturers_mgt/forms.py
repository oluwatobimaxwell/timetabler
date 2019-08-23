from django import forms
from .models import Lecturers, staffTypes
from admin.models import Functions
from departments_mgt.models import Department
from faculty_mgt.models import Faculty



class newLectuerType(forms.ModelForm):
    class Meta:
        model = staffTypes
        fields = '__all__'
        labels = {
            'designation':'Designation',
            'type': ' Priority Number ',
            'LecMaxCosPerSem':' Maximum Contact Hour/Week ',
            'LecMaxCosPerDay':' Maximum Course/Day ',
        }
        widgets = {
            'designation': forms.TextInput(attrs={'class':'form-control p-input'}),
            'type': forms.NumberInput(attrs={'class':'form-control p-input'}),
            'LecMaxCosPerSem': forms.NumberInput(attrs={'class':'form-control p-input'}),
            'LecMaxCosPerDay': forms.NumberInput(attrs={'class':'form-control p-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        newid = Functions.getNewId(staffTypes, '', "{:01}")
        self.fields["type"].initial = newid

class newLecturerForm(forms.ModelForm):
    class Meta:
        model = Lecturers
        fields = "__all__"
        labels = {
            'code' : 'Lecturer ID',
            'name' : 'Lecturer Name',
            'facultyLec' : 'Faculty',
            'departmentLec' : 'Department',
            'priorityNumber' : 'Designation',
            'monFrom' : 'remove',
            'monTo' : 'remove',
            'tueFrom' : 'remove',
            'tueTo' : 'remove',
            'wedFrom' : 'remove',
            'wedTo' : 'remove',
            'thuFrom' : 'remove',
            'thuTo' : 'remove',
            'friFrom' : 'remove',
            'friTo' : 'remove',
            'satFrom' : 'remove',
            'satTo' : 'remove'
        }
        widgets = {
            'code': forms.TextInput(attrs={'class':'form-control p-input', 'readonly':""}),
            'name': forms.TextInput(attrs={'class':'form-control p-input'}),
            'facultyLec': forms.Select(attrs={'data-live-search': 'true', 'class':'form-control p-input populate-drop', 'singular': '1', 'data-source':'faculty', 'data-link':'departmentLec'}),
            'departmentLec': forms.Select(attrs={'data-live-search': 'true', 'class':'form-control p-input'}),
            'monFrom' : forms.TimeInput(format='%H:%M', attrs={'class':'form-control p-input'}),
            'monTo' : forms.TimeInput(format='%H:%M', attrs={'class':'form-control p-input'}),
            'tueFrom' : forms.TimeInput(format='%H:%M', attrs={'class':'form-control p-input'}),
            'tueTo' : forms.TimeInput(format='%H:%M', attrs={'class':'form-control p-input'}),
            'wedFrom' : forms.TimeInput(format='%H:%M', attrs={'class':'form-control p-input'}),
            'wedTo' : forms.TimeInput(format='%H:%M', attrs={'class':'form-control p-input'}),
            'thuFrom' : forms.TimeInput(format='%H:%M', attrs={'class':'form-control p-input'}),
            'thuTo' : forms.TimeInput(format='%H:%M', attrs={'class':'form-control p-input'}),
            'friFrom' : forms.TimeInput(format='%H:%M', attrs={'class':'form-control p-input'}),
            'friTo' : forms.TimeInput(format='%H:%M', attrs={'class':'form-control p-input'}),
            'satFrom' : forms.TimeInput(format='%H:%M', attrs={'class':'form-control p-input'}),
            'satTo' : forms.TimeInput(format='%H:%M', attrs={'class':'form-control p-input'})
        }



    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        newid = Functions.getNewId(Lecturers, 'LEC', "{:04}")
        self.fields["code"].initial = newid

        PRIORITY = []
        for x in range(1, Functions.getMaxPriority()): PRIORITY.append((x,x))
        # self.fields["priorityNumber"] = forms.ChoiceField(label='Priority Number', choices=PRIORITY, required=True, widget=forms.Select(attrs={'class':'form-control p-input'}))
        self.fields["facultyLec"].queryset = Faculty.objects.filter()
        self.fields["departmentLec"].queryset = Department.objects.filter()
