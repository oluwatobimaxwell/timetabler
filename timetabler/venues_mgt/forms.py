from django import forms
from .models import Venue
from admin.models import Functions
from faculty_mgt.models import Faculty

class newVenueForm(forms.ModelForm):

    class Meta:
        model = Venue
        fields = "__all__"
        labels = {
            'code' : 'Venue ID',
            'name' : 'Venue Name',
        }
        widgets = {
            'code': forms.TextInput(attrs={'class':'form-control p-input', 'readonly':""}),
            'name': forms.TextInput(attrs={'class':'form-control p-input'}),
            'capacity': forms.NumberInput(attrs={'class':'form-control p-input'}),
            }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        newid =  Functions.getNewId(Venue, 'VEN', "{:03}")
        self.fields["code"].initial = newid

        CAPACITY = Functions.getVenueTypes()
        self.fields["type"] = forms.ChoiceField(label='Type', choices=CAPACITY, required=False, widget=forms.Select(attrs={'class':'form-control p-input'}))

        LEVELS = Functions.getStudentLevels()
        AVAILABLEDAYS = Functions.getDaysAvailable()
        FACULTIES = Functions.getFacultyList()
        DEPARTMENTS = Functions.getDepartmentList()

        self.fields["reservedDays"] = forms.MultipleChoiceField(label='Days', choices=AVAILABLEDAYS, widget=forms.SelectMultiple(attrs={
                        'class':'selectpicker w-100',
                        'multiple':'multiple',
                        'style':'width:100%',
                        }))

        self.fields["reservedLevel"] = forms.MultipleChoiceField(label='Levels', choices=LEVELS, widget=forms.SelectMultiple(attrs={
                        'class':'selectpicker w-100',
                        'multiple':'multiple',
                        'style':'width:100%',
                        }))

        self.fields["reservedFaculty"] = forms.MultipleChoiceField(label='Faculties', choices=FACULTIES, widget=forms.SelectMultiple(attrs={
                        'class':'selectpicker w-100 populate-drop',
                        'multiple':'multiple',
                        'data-live-search': 'true',
                        'style':'width:100%',
                        'data-source':'faculty',
                        'data-link':'reservedDepartment',
                        'singular': '0',

                        }))

        self.fields["reservedDepartment"] = forms.MultipleChoiceField(label='Departments', choices=DEPARTMENTS, widget=forms.SelectMultiple(attrs={
                        'class':'selectpicker w-100',
                        'multiple':'multiple',
                        'data-live-search': 'true',
                        'style':'width:100%',

                        }))
