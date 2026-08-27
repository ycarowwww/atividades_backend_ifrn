from django import forms

from loja.models import Fabricante


class FabricanteForm(forms.ModelForm):
    class Meta:
        model = Fabricante
        fields = ["Fabricante"]
        widgets = {
            "Fabricante": forms.TextInput(attrs={"class": "form-control"}),
        }
