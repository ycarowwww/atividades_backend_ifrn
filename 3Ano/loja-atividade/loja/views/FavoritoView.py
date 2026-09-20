from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from loja.models import Produto


@login_required
@require_POST
def toggle_favorito_view(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    if produto.favoritos.filter(id=request.user.id).exists():
        produto.favoritos.remove(request.user)
    else:
        produto.favoritos.add(request.user)
    return redirect(request.POST.get("next") or request.META.get("HTTP_REFERER") or "/")


@login_required
def list_favorito_view(request):
    produtos = request.user.produtos_favoritos.all()
    return render(request, "favorito/favorito.html", {"produtos": produtos})
