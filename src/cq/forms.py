from django import forms

from pagedown.widgets import PagedownWidget

from .models import Cq

# datetimepicker
from bootstrap_datepicker_plus import DateTimePickerInput, DatePickerInput


class CqForm(forms.ModelForm):
    question = forms.CharField(widget=PagedownWidget(show_preview=False))
    answer = forms.CharField(widget=PagedownWidget(show_preview=False))
    publish = forms.DateField(widget=DatePickerInput())

    class Meta:
        model = Cq
        fields = [
            "question",
            "image",
            "answer",
            # "level",
            "subject",
            "tags",
            "privacy",
            "draft",
            "publish",
        ]
