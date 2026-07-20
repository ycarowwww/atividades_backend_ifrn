from lojaVeiculo.models import *
class Veiculo(models.Model):
    Veiculo = models.CharField(null=False, max_length=100)
    fabricante = models.CharField(null=False, max_length=100)
    ano = models.PositiveIntegerField()
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)
    def __str__(self):
        return '{}'.format(self.Veiculo)