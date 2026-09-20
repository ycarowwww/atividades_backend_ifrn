from django.shortcuts import render, get_object_or_404, redirect
from loja.models import Produto, Carrinho, CarrinhoItem, Usuario
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils import timezone


def create_carrinhoitem_view(request, produto_id=None):
    produto = get_object_or_404(Produto, pk=produto_id)

    carrinho_id = request.session.get("carrinho_id")
    carrinho = Carrinho.objects.filter(id=carrinho_id).first() if carrinho_id else None
    if carrinho is None or carrinho.situacao != 0:
        carrinho = Carrinho.objects.create()
        request.session["carrinho_id"] = carrinho.id
    carrinho_item = CarrinhoItem.objects.filter(
        carrinho=carrinho, produto=produto
    ).first()
    if carrinho_item:
        carrinho_item.quantidade += 1
    else:
        carrinho_item = CarrinhoItem.objects.create(
            carrinho=carrinho, produto=produto, quantidade=1, preco=produto.preco
        )
    carrinho_item.save()
    return redirect("/carrinho")


def list_carrinho_view(request):
    carrinho = None
    carrinho_item = []
    carrinho_id = request.session.get("carrinho_id")
    if carrinho_id:
        carrinho = Carrinho.objects.filter(id=carrinho_id).first()
        carrinho_item = None
        carrinho_item = CarrinhoItem.objects.filter(carrinho_id=carrinho_id)
    context = {"carrinho": carrinho, "itens": carrinho_item}
    return render(request, "carrinho/carrinho-listar.html", context=context)


@login_required
def confirm_carrinho_view(request):
    carrinho = None
    carrinho_id = request.session.get("carrinho_id")
    if carrinho_id:
        carrinho = Carrinho.objects.filter(id=carrinho_id).first()
        usuario = get_object_or_404(Usuario, user=request.user)
        if usuario:
            carrinho.user = request.user
            carrinho.situacao = 1
            carrinho.confirmado_em = timezone.now()
            carrinho.save()
    itens = carrinho.itens.all() if carrinho else []
    context = {"carrinho": carrinho, "itens": itens}
    return render(request, "carrinho/carrinho-confirmado.html", context=context)


def remove_carrinhoitem_view(request, item_id):
    item = get_object_or_404(CarrinhoItem, id=item_id)
    carrinho_id = request.session.get("carrinho_id")
    if carrinho_id == item.carrinho.id:
        item.delete()
    return redirect("/carrinho")


@require_POST
def change_quantity_carrinhoitem_view(request, item_id, delta):
    item = get_object_or_404(CarrinhoItem, id=item_id)
    carrinho_id = request.session.get("carrinho_id")
    if carrinho_id == item.carrinho_id:
        item.quantidade += delta
        if item.quantidade <= 0:
            item.delete()
        else:
            item.save(update_fields=["quantidade"])
    return redirect("/carrinho")


def increase_carrinhoitem_view(request, item_id):
    return change_quantity_carrinhoitem_view(request, item_id, 1)


def decrease_carrinhoitem_view(request, item_id):
    return change_quantity_carrinhoitem_view(request, item_id, -1)
