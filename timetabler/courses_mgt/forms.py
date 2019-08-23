from django import forms
from .models import Course
from admin.models import Functions

class newCourseForm(forms.ModelForm):

    class Meta:
        model = Course
        fields = "__all__"
        labels = {
            'code' : 'Course Code',
            'name' : 'Course Title',
            'coursehourperweek' : 'Total Hours/Weeks',
        }
        widgets = {
            'code': forms.TextInput(attrs={'class':'form-control p-input'}),
            'name': forms.TextInput(attrs={'class':'form-control p-input'}),
            'coursehourperweek': forms.NumberInput(attrs={'class':'form-control p-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        SUBJECTTYPE = Functions.subjectType()
        self.fields["subjecttype"] = forms.ChoiceField(label='Subject Type', choices=SUBJECTTYPE, required=True, widget=forms.Select(attrs={'class':'form-control p-input'}))

        SEMESTER = Functions.getSemestersList()
        self.fields["semester"] = forms.ChoiceField(label='Semester', choices=SEMESTER, required=Functions.getSemesterReq(), widget=forms.Select(attrs={'class':'form-control p-input'}))

        DEPARTMENTS = Functions.getDepartmentList()
        self.fields["departments"] = forms.MultipleChoiceField(label='Department(s)', choices=DEPARTMENTS, required=True, widget=forms.SelectMultiple(attrs={'class':'form-control p-input populate-drop', 'singular': '0', 'data-source':'department', 'data-link':'lecturers', 'data-live-search': 'true',}))

        LECTURERS = Functions.getLecturerList() #Functions.getLectConfirm(Functions.getLecturerList(), Course)
        self.fields["lecturers"] = forms.MultipleChoiceField(label='Lecturer(s)', choices=LECTURERS, required=False, widget=forms.SelectMultiple(attrs={'class':'form-control p-input', 'data-live-search': 'true'}))
