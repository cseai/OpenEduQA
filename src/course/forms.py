from django import forms
from .models import Subject


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = [
            "level",
            "name",
            "code",
            "short_name",
            "related_names",
            "reladed_levels",
            "ordering_code",
            "medium",
            "description",
            "tags",
            "image",
            "draft",
            "active",
        ]
