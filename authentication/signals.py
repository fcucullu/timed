from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser
from .utils import token_generator

#This signal will create an unique API Key after a new user is created
@receiver(post_save, sender=CustomUser)
def create_api_key(sender, instance, created, **kwargs):
    if created:
        instance.api_key = token_generator.generate_api_key(instance)
        instance.save()  # Saving the instance again to update the API key which is blank by default
