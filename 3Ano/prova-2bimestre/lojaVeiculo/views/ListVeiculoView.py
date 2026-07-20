from django.http import HttpResponse, HttpRequest
from django.shortcuts import render
from lojaVeiculo.models import Veiculo

def list_veiculo_view(request: HttpRequest):
    fabricante = request.GET.get("fabricante")
    ano = request.GET.get("ano")

    veiculos = Veiculo.objects.all()

    if fabricante:
        veiculos = veiculos.filter(fabricante__icontains=fabricante)
    if ano:
        veiculos = veiculos.filter(ano=ano)

    print("=====Veículos Encontrados=====")

    if len(veiculos) > 0:
        for v in veiculos:
            print(f"---{v.Veiculo}---")
            print(f"Fabricante do Veículo: {v.fabricante}")
            print(f"Ano do Veículo: {v.ano}")
    else:
        print("Nenhum Veículo Encontrado")
    
    context = {
        "veiculos": veiculos
    }
    
    return render(request, "home/home.html", context)