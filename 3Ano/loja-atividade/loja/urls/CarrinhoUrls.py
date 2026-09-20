from django.urls import path
from loja.views.CarrinhoView import (
    create_carrinhoitem_view,
    list_carrinho_view,
    confirm_carrinho_view,
    remove_carrinhoitem_view,
    increase_carrinhoitem_view,
    decrease_carrinhoitem_view,
)

urlpatterns = [
    path("", list_carrinho_view, name="list_carrinho"),
    path("<int:produto_id>", create_carrinhoitem_view, name="create_carrinhoitem"),
    path("confirmar", confirm_carrinho_view, name="confirmar_carrinho"),
    path("remover/<int:item_id>/", remove_carrinhoitem_view, name="remover_carrinhoitem"),
    path("aumentar/<int:item_id>/", increase_carrinhoitem_view, name="aumentar_carrinhoitem"),
    path("diminuir/<int:item_id>/", decrease_carrinhoitem_view, name="diminuir_carrinhoitem"),
]
