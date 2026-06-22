from django.urls import path
from .views import home, view_product, create_product, edit_product, delete_product, products

urlpatterns = [
    path("", home, name="home"),
    path("product/<int:pk>/", view_product, name="view_product"),
    path("create_product/", create_product, name="create_product"),
    path("edit_product/<int:pk>/", edit_product, name="edit_product"),
    path("delete_product/<int:pk>/", delete_product, name="delete_product"),
    path("products/", products, name="products"),
]
