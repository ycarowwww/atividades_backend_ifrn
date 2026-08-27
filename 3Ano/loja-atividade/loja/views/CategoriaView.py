from django.shortcuts import get_object_or_404, redirect, render

from loja.models import Categoria


def list_categoria_view(request):
    categorias = Categoria.objects.all()
    return render(
        request,
        "categoria/categoria.html",
        {"categorias": categorias},
        status=200,
    )


def create_categoria_view(request):
    if request.method == "POST":
        categoria = request.POST.get("Categoria", "").strip()
        if categoria:
            Categoria.objects.create(Categoria=categoria)
        return redirect("categoria")
    return render(request, "categoria/categoria-create.html", status=200)


def edit_categoria_view(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == "POST":
        nome = request.POST.get("Categoria", "").strip()
        if nome:
            categoria.Categoria = nome
            categoria.save()
            return redirect("categoria")
    return render(
        request, "categoria/categoria-edit.html", {"categoria": categoria}, status=200
    )


def delete_categoria_view(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    if request.method == "POST":
        categoria.delete()
        return redirect("categoria")
    return render(
        request, "categoria/categoria-delete.html", {"categoria": categoria}, status=200
    )
