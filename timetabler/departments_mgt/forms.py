from django import forms
from .models import Department
from admin.models import Functions
from faculty_mgt.models import Faculty

class newDepartmentForm(forms.ModelForm):

    class Meta:
        model = Department
        fields = "__all__"
        labels = {
            'code' : 'Department ID',
            'name' : 'Department Name',
            'officer_list' : 'Officer',
        }
        widgets = {
            'code': forms.TextInput(attrs={'class':'form-control p-input', 'readonly':""}),
            'name': forms.TextInput(attrs={'class':'form-control p-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        newid = Functions.getNewId(Department, 'DPT', "{:03}")
        self.fields["code"].initial = newid

        CHOICES = Functions.getOfficersList()
        self.fields["officer"] = forms.ChoiceField(choices=CHOICES, required=False, widget=forms.Select(attrs={'data-live-search': 'true','class':'form-control p-input'}))

        self.fields["faculty"].queryset = Faculty.objects.filter()
