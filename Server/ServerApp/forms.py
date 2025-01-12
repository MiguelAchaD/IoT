from django import forms
from .models import Reunion

class ReunionForm(forms.ModelForm):
    class Meta:
        model = Reunion
        fields = ['title', 'description', 'start', 'url']