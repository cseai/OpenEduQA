from django import forms

from pagedown.widgets import PagedownWidget

from django.contrib.postgres.forms import SplitArrayField

from .models import Mcq


# datetimepicker
from bootstrap_datepicker_plus import DateTimePickerInput, DatePickerInput


class McqForm(forms.ModelForm):
    SIZE = 10
    question = forms.CharField(widget=PagedownWidget(css=("pagedown/demo/browser/demo.css", "pagedown/custom/small.css",), show_preview=False))
    # choices = forms.CharField(widget=PagedownWidget(show_preview=False))
    # answer = forms.CharField(widget=PagedownWidget(show_preview=False))
    # total_choices = forms.IntegerField()
    choices = forms.CharField()
    choices = SplitArrayField(forms.CharField(required=False), size=SIZE, remove_trailing_nulls=True, required=False)  # size=5,
    # choices = SplitArrayField(forms.CharField(widget=PagedownWidget(css=("pagedown/demo/browser/demo.css", "pagedown/custom/small.css",),show_preview=False), required=False), size=SIZE, remove_trailing_nulls=False)  # size=5,
    publish = forms.DateField(widget=DatePickerInput())

    class Meta:
        model = Mcq
        fields = [
            "question",
            "image",
            "choices",
            # 'total_choices',
            "answer",
            # "level",
            "subject",
            "tags",
            'privacy',
            "draft",
            "publish",
        ]


class McqAddForm(forms.ModelForm):
    choices = SplitArrayField(forms.CharField(required=True), size=2, remove_trailing_nulls=True)  # size=5,

    class Meta:
        model = Mcq
        fields = [
            "choices",
            "answer",
        ]
