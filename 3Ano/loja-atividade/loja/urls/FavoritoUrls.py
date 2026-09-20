from django.urls import path

from loja.views.FavoritoView import toggle_favorito_view, list_favorito_view

urlpatterns = [
    path("", list_favorito_view, name="listar_favoritos"),
    path("alternar/<int:produto_id>/", toggle_favorito_view, name="alternar_favorito"),
]
