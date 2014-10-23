from django import forms

DATE_HELP_STR = "Dates must be of the form YYYY-MM-DD"

class StartEndDateForm(forms.Form):
    start_date = forms.DateField(label="Start date:",
                                 required=True,
                                 help_text=DATE_HELP_STR,
                                 input_formats=["%Y-%m-%d"])
    end_date = forms.DateField(label="End date:",
                               required=True,
                               input_formats=["%Y-%m-%d"])
