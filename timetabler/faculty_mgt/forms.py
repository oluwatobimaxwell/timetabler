from django import forms
from .models import Faculty
from admin.models import Functions
# from django.forms import widgets


class newFacultyForm(forms.ModelForm):
    CHOICES = Functions.getOfficersList()
    officer = forms.ChoiceField(choices=CHOICES, required=False, widget=forms.Select(attrs={'class':'form-control p-input'}))

    class Meta:
        model = Faculty
        fields = ["code", "name", "officer", "image"]
        labels = {
            'code' : 'Faculty ID',
            'name' : 'Faculty Name',
            'officer_list' : 'Officer',
            'image': 'Display Image',
        }
        widgets = {
            'code': forms.TextInput(attrs={'class':'form-control p-input', 'readonly':""}),
            'name': forms.TextInput(attrs={'class':'form-control p-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['image'].widget.attrs['data-default-file'] = ''
        self.fields['image'].widget.attrs['class'] = 'dropify'

        newid = Functions.getNewId(Faculty, 'FAC', "{:02}")
        self.fields["code"].initial = newid

        CHOICES = Functions.getOfficersList()
        self.fields["officer"] = forms.ChoiceField(choices=CHOICES, required=False, widget=forms.Select(attrs={'data-live-search': 'true','class':'form-control p-input'}))
