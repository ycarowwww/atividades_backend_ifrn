from django.urls import path
from lojaVeiculo.views.HomeView import home_view
from lojaVeiculo.views.ListVeiculoView import list_veiculo_view

urlpatterns = [
    path("", list_veiculo_view),
]