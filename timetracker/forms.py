from django import forms


class AddForm(forms.Form):
    details = forms.CharField(max_length=200, required=False)
    start_date = forms.CharField(required=False)
    
    rate = forms.CharField(required=False)
    time = forms.CharField(required=False)
    start_time_hours = forms.CharField(required=False)
    start_time_mins = forms.CharField(required=False)
    start_time_ampm = forms.CharField(required=False)
    client = forms.CharField(required=False)
    name = forms.CharField(required=False)
    currency = forms.CharField(required=False)


class MakeURLForm(forms.Form):
    can_write = forms.BooleanField(required=False)
    can_see_names = forms.BooleanField(required=False)
    can_see_details = forms.BooleanField(required=False)
