from django import forms
from .models import Reunion

class ReunionForm(forms.ModelForm):
    class Meta:
        model = Reunion
        fields = ['titulo', 'descripcion', 'fecha', 'enlace']