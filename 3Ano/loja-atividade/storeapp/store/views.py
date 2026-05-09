from django.db.models.query import QuerySet
from django.views import generic
from .models import Product
from typing import Any

class IndexView(generic.ListView):
    template_name = "store/index.html"
    context_object_name = "products"

    def get_queryset(self) -> QuerySet[Any]:
        return Product.objects.all()
    
class ProductView(generic.DetailView):
    model = Product
    template_name = "store/product.html"
