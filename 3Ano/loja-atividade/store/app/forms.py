from django import forms
from django.contrib.auth.models import User
from .models import Product, UserModel, Manufacturer
from .widgets import ImagePreviewInput

class UserModelForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(UserModelForm, self).__init__(*args, **kwargs)

        if self.instance and self.instance.profile != 1:
            del self.fields["profile"]
    
    class Meta:
        model = UserModel
        fields = ["user", "profile", "birthday"]
        widgets = {
            "user": forms.HiddenInput(),
            "profile": forms.Select(attrs={"class": "form-control"}),
            "birthday": forms.DateInput(attrs={
                    "class":"form-control", 
                    "type": "date"
                }
            )
        }

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "first_name": forms.TextInput(attrs={"class": "form-control"}),
            "last_name": forms.TextInput(attrs={"class": "form-control"})
        }

class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = Manufacturer
        fields = ["name"]
        labels = {
            "name": "Nome"
        }
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control"})
        }

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = "__all__"
        labels = {
            "name": "Nome",
            "is_highlighted": "É Destacado",
            "in_promotion": "Em Promoção",
            "promotion_message": "Mensagem da Promoção",
            "price": "Preço",
            "manufacturer": "Fabricante",
            "categories": "Categorias",
            "image": "Imagem"
        }
        widgets = {
            "image": ImagePreviewInput(attrs={"accept": "image/*"})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove ":" from all fields.
        self.label_suffix = ""
