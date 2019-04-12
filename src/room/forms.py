from django import forms

from pagedown.widgets import PagedownWidget

# from django.contrib.postgres.forms import SplitArrayField

from .models import Room


# datetimepicker
from bootstrap_datepicker_plus import DateTimePickerInput, DatePickerInput
# from django.views import generic


class RoomForm(forms.ModelForm):
    description = forms.CharField(widget=PagedownWidget(show_preview=False))
    # choices = SplitArrayField(forms.CharField(required=True), size=5, remove_trailing_nulls=True)  # size=5,
    publish = forms.DateField(widget=DatePickerInput())
    happen = forms.DateTimeField(widget=DateTimePickerInput())

    class Meta:
        model = Room
        fields = [
            "title",
            "description",
            "image",
            "exam",
            "teachers",
            "students",
            "tags",
            'duration',
            'happen',
            'draft',
            'privacy',
            'publish',
        ]
