from django import forms

from pagedown.widgets import PagedownWidget

# from django.contrib.postgres.forms import SplitArrayField

from .models import McqExam

# datetimepicker
from bootstrap_datepicker_plus import DateTimePickerInput, DatePickerInput


class McqExamForm(forms.ModelForm):
    description = forms.CharField(widget=PagedownWidget(show_preview=False))
    # choices = SplitArrayField(forms.CharField(required=True), size=5, remove_trailing_nulls=True)  # size=5,
    publish = forms.DateField(widget=DatePickerInput())

    class Meta:
        model = McqExam
        fields = [
            "title",
            "description",
            "image",
            # "level",
            "subject",
            "tags",
            'setname',
            'items',
            'mark',
            'duration',
            'qlist',
            'privacy',
            "draft",
            "publish",
        ]
