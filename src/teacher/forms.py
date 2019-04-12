# accounts.forms.py
from django import forms

from .models import Teacher
from datetime import date
# from .models import User
from course.models import Subject

# datetimepicker
from bootstrap_datepicker_plus import DateTimePickerInput, DatePickerInput


class TeacherUpdateForm(forms.ModelForm):
    # since = forms.DateField(widget=forms.SelectDateWidget(empty_label="Nothing"))
    _today = date.today()
    _years = [x for x in range(_today.year, 1950, -1)]
    # since = forms.DateField(
    #     widget=forms.SelectDateWidget(
    #         years=_years,
    #         # empty_label=("Choose Year", "Choose Month", "Choose Day"),
    #     ),
    #     required=False
    # )

    since = forms.DateField(widget=DatePickerInput())

    class Meta:
        model = Teacher
        fields = (
            'since',
            'courses',
            'seeking_job',
            'cv_file',
            'current_workplaces',
            'past_workplaces',
            # 'active',
        )

    def __init__(self, *args, **kwargs):
        super(TeacherUpdateForm, self).__init__(*args, **kwargs)
        self.fields['courses'].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["courses"].queryset = Subject.objects.all()

    def save(self, commit=True):
        teacher = super(TeacherUpdateForm, self).save(commit=False)

        if commit:
            teacher.save()
        return teacher
