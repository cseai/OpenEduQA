from django import forms

from pagedown.widgets import PagedownWidget

from .models import Article

# datetimepicker
from bootstrap_datepicker_plus import DateTimePickerInput, DatePickerInput


class ArticleForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))
    publish = forms.DateField(widget=DatePickerInput)

    class Meta:
        model = Article
        fields = [
            "title",
            "content",
            "image",
            "draft",
            "publish",
            # "level",
            "subject",
            "tags",
        ]
