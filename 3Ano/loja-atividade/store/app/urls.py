from django.urls import path
from .views import (
    home, view_product, create_product, edit_product, delete_product,
    products, users, edit_user,
    categories, create_category, edit_category, delete_category,
    manufacturers, create_manufacturer, edit_manufacturer, delete_manufacturer,
)

urlpatterns = [
    path("", home, name="home"),
    path("product/<int:pk>/", view_product, name="view_product"),
    path("create_product/", create_product, name="create_product"),
    path("edit_product/<int:pk>/", edit_product, name="edit_product"),
    path("delete_product/<int:pk>/", delete_product, name="delete_product"),
    path("products/", products, name="products"),
    path("users/", users, name="users"),
    path("edit_user/", edit_user, name="edit_user"),
    path("categories/", categories, name="categories"),
    path("create_category/", create_category, name="create_category"),
    path("edit_category/<int:pk>/", edit_category, name="edit_category"),
    path("delete_category/<int:pk>/", delete_category, name="delete_category"),
    path("manufacturers/", manufacturers, name="manufacturers"),
    path("create_manufacturer/", create_manufacturer, name="create_manufacturer"),
    path("edit_manufacturer/<int:pk>/", edit_manufacturer, name="edit_manufacturer"),
    path("delete_manufacturer/<int:pk>/", delete_manufacturer, name="delete_manufacturer"),
]
