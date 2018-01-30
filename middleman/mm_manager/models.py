from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class GarlicUser(models.Model):
    user = models.OneToOneField(User, models.CASCADE)
    address = models.CharField(max_length=35)
    

class Middleman(models.Model):
    # OneToOne is here so that if User is deleted, Middleman is deleted too,
    # but not the reverse
    garlic_user = models.OneToOneField(GarlicUser, models.CASCADE)

    rating = models.FloatField()
    fee = models.FloatField()

@receiver(post_save, sender=User)
def create_garlic_user(sender, instance, created, **kwargs):
    if created:
        GarlicUser.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_garlic_user(sender, instance, **kwargs):
    instance.profile.save()