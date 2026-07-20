import os
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, post_delete
from django.dispatch import receiver

PROFILE = (
    (1, 'Admin'),
    (2, 'Usuario')
)

class UserModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile = models.IntegerField(choices=PROFILE, default=2)
    birthday = models.DateField(default=None, null=True, blank=True)
    created_in = models.DateTimeField(auto_now_add=True)
    changed_in = models.DateTimeField(auto_now=True)
    token = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.user.username}'
    
    @receiver(post_save, sender=User)
    def create_user_usuario(sender, instance, created, **kwargs):
        try:
            if created:
                UserModel.objects.create(user=instance)
        except:
            pass

    @receiver(post_save, sender=User)
    def save_user_usuario(sender, instance, **kwargs):
        try:
            instance.usuario.save()
        except:
            pass

class Manufacturer(models.Model):
    name = models.CharField(null=False, max_length=127)
    created_in = models.DateTimeField(auto_now_add=True)
    modified_in = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.id} - {self.name}" # type: ignore

class Category(models.Model):
    name = models.CharField(null=False, max_length=127)
    created_in = models.DateTimeField(auto_now_add=True)
    modified_in = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"{self.id} - {self.name}" # type: ignore
    
class Product(models.Model):
    name = models.CharField(null=False, max_length=127)
    is_highlighted = models.BooleanField(default=True)
    in_promotion = models.BooleanField(default=True)
    promotion_message = models.CharField(blank=True, max_length=127)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    categories = models.ManyToManyField(Category)
    image = models.ImageField(upload_to="products/", blank=False, null=False)

    def __str__(self) -> str:
        return f"{self.id} - {self.name}" # type: ignore

# Deletes the old image's file when updated
@receiver(pre_save, sender=Product)
def delete_old_file_on_change(sender, instance, **kwargs):
    if not instance.pk:
        return False

    try:
        old_file = sender.objects.get(pk=instance.pk).image
    except sender.DoesNotExist:
        return False

    new_file = instance.image
    if old_file and old_file != new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)

# Deletes the image when the entire model is deleted.
@receiver(post_delete, sender=Product)
def delete_file_on_instance_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)
