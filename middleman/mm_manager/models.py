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

    rating = models.FloatField(null=True)
    fee = models.FloatField(null=True)
    bio = models.CharField(max_length=256, null=True)

    def __str__(self):
        return '{}: {}% ✔ ({}GRLC)'.format(self.garlic_user.user.username, self.rating, self.fee)

class Trade(models.Model):
    item_1 = models.CharField(max_length=64)
    item_2 = models.CharField(max_length=64)
    
    person_1 = models.CharField(max_length=64)
    person_2 = models.CharField(max_length=64)
    middleman = models.ForeignKey(Middleman, models.CASCADE)
    
    time_created = models.DateTimeField()
    time_mm_received_1 = models.DateTimeField(null=True)
    time_mm_received_2 = models.DateTimeField(null=True)
    time_mm_completed = models.DateTimeField(null=True)

@receiver(post_save, sender=User)
def save_user_garlicuser(sender, instance, **kwargs):
    if instance.garlicuser == None:
        GarlicUser.objects.create(user=instance)
    instance.garlicuser.save()