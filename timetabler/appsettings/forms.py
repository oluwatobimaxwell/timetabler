from django import forms
from .models import appSettings
from admin.models import Functions

class AppSettingsForm(forms.ModelForm):

    class Meta:
        model = appSettings
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        ADMISSIONTYPE = Functions.AdmissionType()
        self.fields["admissionType"] = forms.ChoiceField(label='Semester', choices=ADMISSIONTYPE, required=True, widget=forms.RadioSelect(attrs={'class':'form-control p-input', 'onchange':'checkadmtype(this.value)'}))

        SESSIONLIST = Functions.SessionList()
        self.fields["currentsession"] = forms.ChoiceField(choices=SESSIONLIST, required=True, widget=forms.Select(attrs={'class':'form-control p-input'}))

        SEMESTERNAME = Functions.getSemesterAlias()
        self.fields["currentsemestername"] = forms.ChoiceField(choices=SEMESTERNAME, required=True, widget=forms.Select(attrs={'class':'form-control p-input'}))

        SEMESTERTYPE = Functions.getSemestersList()
        self.fields["currentsemestertype"] = forms.ChoiceField(choices=SEMESTERTYPE, required=True, widget=forms.Select(attrs={'class':'form-control p-input'}))

        # LECTURERS = Functions.getLecturerList()
        # self.fields["lecturers"] = forms.MultipleChoiceField(label='Lecturer(s)', choices=LECTURERS, required=True, widget=forms.SelectMultiple(attrs={'class':'form-control p-input', 'data-live-search': 'true'}))
