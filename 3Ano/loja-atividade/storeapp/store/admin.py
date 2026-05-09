from django.contrib import admin
from .models import Category, Manufacturer, Product

class CategoryAndManufacturerAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["name"]})
    ]
    list_display = ["id", "name"]

class ProductAdmin(admin.ModelAdmin):
    fieldsets = [
        ("Base Information", {"fields": ["name", "manufacturer", "categories"]}),
        ("Price Information", {"fields": ["price", "promotion", "is_featured"]}),
        ("Other Information", {"fields": ["image"]})
    ]
    list_display = ["name", "manufacturer", "price"]

admin.site.register([Category, Manufacturer], CategoryAndManufacturerAdmin)
admin.site.register(Product, ProductAdmin)
