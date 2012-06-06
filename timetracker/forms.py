from django import forms
from timetracker.models import CLIENT_CHOICES


class AddForm(forms.Form):
    details = forms.CharField(max_length=200)
    start_date = forms.CharField(required=False)
