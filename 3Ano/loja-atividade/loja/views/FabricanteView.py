from django.shortcuts import get_object_or_404, redirect, render

from loja.forms.FabricanteForm import FabricanteForm
from loja.models import Fabricante


def list_fabricante_view(request):
    fabricantes = Fabricante.objects.all()
    return render(
        request,
        "fabricante/fabricante.html",
        {"fabricantes": fabricantes},
        status=200,
    )


def create_fabricante_view(request):
    fabricante_form = FabricanteForm(request.POST or None)
    if request.method == "POST" and fabricante_form.is_valid():
        fabricante_form.save()
        return redirect("fabricante")
    return render(
        request,
        "fabricante/fabricante-form.html",
        {"fabricanteForm": fabricante_form, "titulo": "Novo Fabricante"},
        status=200,
    )


def edit_fabricante_view(request, id):
    fabricante = get_object_or_404(Fabricante, id=id)
    fabricante_form = FabricanteForm(request.POST or None, instance=fabricante)
    if request.method == "POST" and fabricante_form.is_valid():
        fabricante_form.save()
        return redirect("fabricante")
    return render(
        request,
        "fabricante/fabricante-form.html",
        {"fabricanteForm": fabricante_form, "titulo": "Editar Fabricante"},
        status=200,
    )


def delete_fabricante_view(request, id):
    fabricante = get_object_or_404(Fabricante, id=id)
    if request.method == "POST":
        fabricante.delete()
        return redirect("fabricante")
    return render(
        request,
        "fabricante/fabricante-delete.html",
        {"fabricante": fabricante},
        status=200,
    )
