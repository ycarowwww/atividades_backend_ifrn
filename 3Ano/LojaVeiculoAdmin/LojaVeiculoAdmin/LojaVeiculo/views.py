from django.shortcuts import render
from django.http import HttpRequest, HttpResponse

# Create your views here.
def list_veiculo_view(request: HttpRequest) -> HttpResponse:
    return HttpResponse("<h1>Lista de Veículos</h1>")
