from django import forms

from pagedown.widgets import PagedownWidget

# from django.contrib.postgres.forms import SplitArrayField

from .models import Exam


# datetimepicker
from bootstrap_datepicker_plus import DateTimePickerInput, DatePickerInput


class ExamForm(forms.ModelForm):
    description = forms.CharField(widget=PagedownWidget(show_preview=False))
    # choices = SplitArrayField(forms.CharField(required=True), size=5, remove_trailing_nulls=True)  # size=5,
    publish = forms.DateField(widget=DatePickerInput())

    class Meta:
        model = Exam
        fields = [
            "title",
            "description",
            "image",
            # "levels",
            "subjects",
            "tags",
            'setname',
            'items',
            'mark',
            'duration',
            'hascq',
            'hasmcq',
            'cqelist',
            'mcqelist',
            'privacy',
            "draft",
            "publish",
        ]
