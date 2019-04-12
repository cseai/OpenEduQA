# accounts.forms.py
from django import forms

from .models import Student
from datetime import date
from course.models import Subject

# datetimepicker
from bootstrap_datepicker_plus import DateTimePickerInput, DatePickerInput


class StudentUpdateForm(forms.ModelForm):
    # since = forms.DateField(widget=forms.SelectDateWidget(empty_label="Nothing"))
    _today = date.today()
    _years = [x for x in range(_today.year, 1940, -1)]
    # since = forms.DateField(
    #     widget=forms.SelectDateWidget(
    #         years=_years,
    #         # empty_label=("Choose Year", "Choose Month", "Choose Day"),
    #     ),
    #     required=False
    # )

    since = forms.DateField(widget=DatePickerInput())

    class Meta:
        model = Student
        fields = (
            'since',
            'current_courses',
            'completed_courses',
            # 'student_bio',
            'seeking_job',
            'cv_file',
            'current_workplaces',
            'past_workplaces',
            'offer_notification_on',
            # 'active',
        )

    def __init__(self, *args, **kwargs):
        super(StudentUpdateForm, self).__init__(*args, **kwargs)
        self.fields['current_courses'].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["current_courses"].queryset = Subject.objects.all()
        self.fields['completed_courses'].widget = forms.widgets.CheckboxSelectMultiple()
        self.fields["completed_courses"].queryset = Subject.objects.all()

    def save(self, commit=True):
        student = super(StudentUpdateForm, self).save(commit=False)

        if commit:
            student.save()
        return student
