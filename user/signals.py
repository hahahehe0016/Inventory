from urllib import request
from django.contrib.auth.models import User
from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, DELETION
from dashboard.actions import log_addition
from .models import Profile, User
from dashboard.models import Product, Order, Component, Allocation, Employee
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.contenttypes.models import ContentType
from django.utils.encoding import force_str

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(employee=instance)


@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
        instance.profile.save
        print(instance)


@receiver(post_save, sender=Product)
def save_product(sender, instance, created, **kwargs):
    if created:
        print("Test")
    else:
        print("Log_change")

@receiver(post_save, sender=Allocation)
def save_allocation(sender, instance, created, **kwargs):
    if created:
        print("Test")
    else:
        print("Log_change")

@receiver(post_delete, sender=Product)
def delete_product(sender, instance, **kwargs):
    print("Log_delete")

    
        

