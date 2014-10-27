from django import forms
from django.core.exceptions import ValidationError

DATE_HELP_STR = "Dates must be of the form YYYY-MM-DD"

def date_order_validator(start_date, end_date):
    """Throws a validation error if the end date is before the start date"""
    if end_date < start_date:
        raise ValidationError("End date cannot be before Start date",
                code="date order")

class StartEndDateForm(forms.Form):
    start_date = forms.DateField(label="Start date:",
                                 required=True,
                                 help_text=DATE_HELP_STR,
                                 input_formats=["%Y-%m-%d"])
    end_date = forms.DateField(label="End date:",
                               required=True,
                               input_formats=["%Y-%m-%d"])

    def clean(self):
        """Perform validation between fields"""
        # Perform parent validations
        cleaned_data = super(StartEndDateForm, self).clean()
        try:
            clean_start = cleaned_data["start_date"]
            clean_end = cleaned_data["end_date"]
            date_order_validator(clean_start, clean_end)
        except KeyError:
            pass

