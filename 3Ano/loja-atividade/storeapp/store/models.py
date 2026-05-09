from django.db import models

# Product, Manufacturer, Category
class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f"{self.id} - {self.name}" # type: ignore

class Manufacturer(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self) -> str:
        return f"{self.id} - {self.name}" # type: ignore

class Product(models.Model):
    name = models.CharField(max_length=128)
    is_featured = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    promotion = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to="product_pics/", default="product_pics/default.png", null=True, blank=True)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)

    def __str__(self) -> str:
        return f"{self.id} - {self.name}" # type: ignore
