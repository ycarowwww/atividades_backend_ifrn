from django.db import models

# Create your models here.
class Veiculo(models.Model):
    descricao = models.CharField("Descrição", max_length=256)
    cor = models.CharField("Cor", max_length=256)
    ano = models.IntegerField("Ano")
    preco = models.FloatField("Preço")

    def __str__(self):
        return f"Veículo {self.descricao} {self.cor} {self.ano} - R${self.preco}"
