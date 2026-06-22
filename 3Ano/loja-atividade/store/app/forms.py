from django import forms
from .models import Product
from .widgets import ImagePreviewInput

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
            "image": ImagePreviewInput(attrs={'accept': 'image/*'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove ":" from all fields.
        self.label_suffix = ""
