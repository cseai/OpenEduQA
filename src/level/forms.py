from django import forms
from .models import Level


class LevelForm(forms.ModelForm):
    class Meta:
        model = Level
        fields = [
            "name",
            "code",
            "short_name",
            "related_names",
            "ordering_code",
            "description",
            "tags",
            "image",
            "draft",
            "active",
        ]
