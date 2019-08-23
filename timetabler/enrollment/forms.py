from django import forms
from .models import Enrolment
from admin.models import Functions
# from faculty_mgt.models import Faculty

class BulkDataUpload(forms.ModelForm):

    class Meta:
        model = Enrolment
        fields = ['session', 'semesterType', 'code']
        labels = {
            'code': 'Upload File'
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['code'].widget.attrs['data-default-file'] = ''
        self.fields['code'].widget.attrs['class'] = 'dropify'

        SESSION = Functions.SessionList()
        self.fields["session"] = forms.ChoiceField(label='Session',choices=SESSION, required=False, widget=forms.Select(attrs={'class':'form-control p-input'}))

        SEMESTERTYPE = Functions.getSemestersList()
        self.fields["semesterType"] = forms.ChoiceField(label='Semester Type', choices=SEMESTERTYPE, required=False, widget=forms.Select(attrs={'class':'form-control p-input'}))


class EnrolmentForm(forms.ModelForm):

    class Meta:
        model = Enrolment
        fields = "__all__"
        labels = {
            'code':'Enrolment ID',
            'course_code': 'Course',
            'student_id': 'Student ID',
            'semesterName': 'Semester Name',
            'semesterType': 'Semester Type',
            'department': 'Department',
            'level': 'Level',
        }
        widgets = {
            'code': forms.TextInput(attrs={'class':'form-control p-input', 'readonly':"",}),
            'student_id': forms.TextInput(attrs={'class':'form-control p-input'}),
            'course_code': forms.Select(attrs={'data-live-search': 'true'}),
            'department': forms.Select(attrs={'data-live-search': 'true'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        newid = Functions.getNewId(Enrolment, 'ENR', "{:07}")
        self.fields["code"].initial = newid

        SESSION = Functions.SessionList()
        self.fields["session"] = forms.ChoiceField(choices=SESSION, required=False, widget=forms.Select(attrs={'class':'form-control p-input'}))

        SEMESTERNAME = Functions.getSemesterAlias()
        self.fields["semesterName"] = forms.ChoiceField(label='Semester Name',choices=SEMESTERNAME, required=False, widget=forms.Select(attrs={'class':'form-control p-input'}))

        SEMESTERTYPE = Functions.getSemestersList()
        self.fields["semesterType"] = forms.ChoiceField(label='Semester Type', choices=SEMESTERTYPE, required=False, widget=forms.Select(attrs={'class':'form-control p-input'}))

        LEVEL = Functions.getStudentLevels()
        self.fields["level"] = forms.ChoiceField(choices=LEVEL, required=False, widget=forms.Select(attrs={'class':'form-control p-input'}))

        # self.fields["course_code"].widget = forms.Select(attrs={'data-live-search': 'true'})
