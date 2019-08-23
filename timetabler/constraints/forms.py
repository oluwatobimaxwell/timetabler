from django import forms
from .models import UserConstraints
from admin.models import Functions

class ConstraintsForm(forms.ModelForm):

    class Meta:
        model = UserConstraints
        fields = "__all__"
        widgets = {
            'LectureStartTime' : forms.TimeInput(format='%H:%M', attrs={'class':'form-control p-input'}),
            'LectureCloseTime' : forms.TimeInput(format='%H:%M', attrs={'class':'form-control p-input'}),
            'DailyBrkStartTime' : forms.TimeInput(format='%H:%M', attrs={'class':'form-control p-input'}),
            'DailyBrkDuration' : forms.TextInput(attrs={'class':'form-control p-input'}),
            'MuslimPrayStart' : forms.TimeInput(format='%H:%M', attrs={'class':'form-control p-input'}),
            'MuslimPrayDuration' : forms.TextInput(attrs={'class':'form-control p-input'}),
            'LecMaxCosPerSem' : forms.TextInput(attrs={'class':'form-control p-input'}),
            'LecMaxClassPerDay' : forms.TextInput(attrs={'class':'form-control p-input'}),
            'LecMinBtwClasses' : forms.TextInput(attrs={'class':'form-control p-input'}),
            'StuMaxClassPerDay' : forms.TextInput(attrs={'class':'form-control p-input'}),
            'StuMinBtwClasses' : forms.TextInput(attrs={'class':'form-control p-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["LectureStartTime"].initial = '09:00'
        self.fields["LectureCloseTime"].initial = '18:00'
        self.fields["DailyBrkStartTime"].initial = '13:00'
        self.fields["MuslimPrayStart"].initial = '12:30'
        #
        # SEMESTER = Functions.getSemestersList()
        # self.fields["semester"] = forms.ChoiceField(label='Semester', choices=SEMESTER, required=Functions.getSemesterReq(), widget=forms.Select(attrs={'class':'form-control p-input'}))
        #
        # DEPARTMENTS = Functions.getDepartmentList()
        # self.fields["departments"] = forms.MultipleChoiceField(label='Department(s)', choices=DEPARTMENTS, required=True, widget=forms.SelectMultiple(attrs={'class':'form-control p-input populate-drop', 'singular': '0', 'data-source':'department', 'data-link':'lecturers', 'data-live-search': 'true',}))
        #
        # LECTURERS = Functions.getLecturerList()
        # self.fields["lecturers"] = forms.MultipleChoiceField(label='Lecturer(s)', choices=LECTURERS, required=True, widget=forms.SelectMultiple(attrs={'class':'form-control p-input', 'data-live-search': 'true'}))
