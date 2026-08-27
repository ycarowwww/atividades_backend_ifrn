from django.db import models
from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from loja.models import Categoria, Fabricante


class Produto(models.Model):
    Produto = models.CharField(null=False, max_length=100)
    destaque = models.BooleanField(default=True)
    promocao = models.BooleanField(default=True)
    msgPromocao = models.CharField(null=True, max_length=100, blank=True)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    categoria = models.ForeignKey(
        Categoria, null=True, related_name="categoria", on_delete=models.SET_NULL
    )
    fabricante = models.ForeignKey(
        Fabricante, null=True, related_name="fabricante", on_delete=models.SET_NULL
    )
    criado_em = models.DateTimeField(auto_now_add=True)
    alterado_em = models.DateTimeField(auto_now=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"{self.Produto}"


@receiver(pre_save, sender=Produto)
def delete_replaced_product_image(sender, instance, **kwargs):
    if not instance.pk:
        return

    old_instance = sender.objects.filter(pk=instance.pk).first()
    if (
        old_instance
        and old_instance.image
        and old_instance.image.name != instance.image.name
    ):
        old_instance.image.delete(save=False)


@receiver(post_delete, sender=Produto)
def delete_product_image(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(save=False)
