from django import forms
from .models import TableRegister, TablesGenerated
from admin.models import Functions
from venues_mgt.models import Venue

def getVenueList():
    all = Venue.objects.all()
    params = [('','----------')]
    for item in all:
        params.append((item.code,item.name))
    return params

class manualSchedulerForm(forms.ModelForm):

    class Meta:
        model = TablesGenerated
        fields = ['code','groupid','starttime','endtime','venue', 'lectureday']
        widgets = {
            'starttime': forms.TextInput(attrs={'class':'form-control p-input'}),
            'endtime': forms.TextInput(attrs={'class':'form-control p-input'}),
            'venue': forms.TextInput(attrs={'class':'form-control p-input'}),
            'lectureday': forms.TextInput(attrs={'class':'form-control p-input'}),
        }


    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        DAYS = Functions.getDaysAvailable()
        self.fields["lectureday"] = forms.ChoiceField(choices=DAYS, required=True, widget=forms.Select(attrs={'class':'form-control p-input'}))

        VENUES = getVenueList()
        self.fields["venue"] = forms.ChoiceField(choices=VENUES, required=True, widget=forms.Select(attrs={'class':'form-control p-input'}))





class generateForm(forms.ModelForm):

    class Meta:
        model = TableRegister
        fields = ['code', 'session', 'semestername', 'semestertype']

        widgets = {
            'code': forms.TextInput(attrs={'class':'form-control p-input', 'style':'display:none;', 'readonly':""}),
            # 'name': forms.TextInput(attrs={'class':'form-control p-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        newid =  Functions.getNewId(TableRegister, 'TBL', "{:07}")
        self.fields["code"].initial = newid

        SESSION = Functions.SessionList()
        self.fields["session"] = forms.ChoiceField(initial=Functions.getSettingsData('session'), choices=SESSION, required=True, widget=forms.Select(attrs={'class':'form-control p-input'}))

        SEMESTERNAME = Functions.getSemesterAlias()
        self.fields["semestername"] = forms.ChoiceField(label='Semester', initial=Functions.getSettingsData('semname'), choices=SEMESTERNAME, required=not(Functions.getSemesterReq()), widget=forms.Select(attrs={'class':'form-control p-input'}))

        SEMESTERTYPE = Functions.getSemestersList()
        self.fields["semestertype"] = forms.ChoiceField(label='Semester', initial=Functions.getSettingsData('semtype'), choices=SEMESTERTYPE, required=Functions.getSemesterReq(), widget=forms.Select(attrs={'class':'form-control p-input'}))
