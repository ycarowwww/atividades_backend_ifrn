from django.urls import path
from . import views

urlpatterns = [
    path("", views.list_veiculo_view, name="list_veiculo_view")
]
