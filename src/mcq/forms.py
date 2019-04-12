from django import forms

from pagedown.widgets import PagedownWidget

from django.contrib.postgres.forms import SplitArrayField

from .models import Mcq


# datetimepicker
from bootstrap_datepicker_plus import DateTimePickerInput, DatePickerInput


class McqForm(forms.ModelForm):
    question = forms.CharField(widget=PagedownWidget(show_preview=False))
    # choices = forms.CharField(widget=PagedownWidget(show_preview=False))
    # answer = forms.CharField(widget=PagedownWidget(show_preview=False))
    choices = SplitArrayField(forms.CharField(required=True), size=4, remove_trailing_nulls=True)  # size=5,
    publish = forms.DateField(widget=DatePickerInput())

    class Meta:
        model = Mcq
        fields = [
            "question",
            "image",
            "choices",
            "answer",
            # "level",
            "subject",
            "tags",
            'privacy',
            "draft",
            "publish",
        ]
