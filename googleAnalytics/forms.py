from django import forms

class StartEndDateForm(forms.Form):
    start_date = forms.DateField(label="Start date:",
                                 required=True,
                                 input_formats=["%Y-%m-%d"])
    end_date = forms.DateField(label="End date:",
                               required=True,
                               input_formats=["%Y-%m-%d"])
