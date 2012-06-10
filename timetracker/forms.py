from django import forms


class AddForm(forms.Form):
    details = forms.CharField(max_length=200)
    start_date = forms.CharField(required=False)


class MakeURLForm(forms.Form):
    can_write = forms.BooleanField(required=False)
    can_see_names = forms.BooleanField(required=False)
    can_see_details = forms.BooleanField(required=False)
