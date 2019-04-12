from django import forms

from pagedown.widgets import PagedownWidget

from .models import Post

# datetimepicker
from bootstrap_datepicker_plus import DateTimePickerInput, DatePickerInput


class PostForm(forms.ModelForm):
    content = forms.CharField(widget=PagedownWidget(show_preview=False))
    publish = forms.DateField(widget=DatePickerInput())

    class Meta:
        model = Post
        fields = [
            "title",
            "content",
            "image",
            "draft",
            "publish",
        ]
