import requests

from django.db.models.signals import post_save
from django.dispatch import receiver

from project.projects.models import Project
from ypm import settings


@receiver(post_save, sender=Project)
def project_created(sender, instance, created, **kwargs):
    # if created:
    #     url = settings.AI_SERVER_URL + '/project/'
    #     data = {
    #         'name': instance.name,
    #         'description': instance.description,
    #     }
    #     try:
    #         response = requests.post(url, json=data)
    #         response.raise_for_status()
    #     except requests.exceptions.RequestException as e:
    #         print(f"Error al realizar la petición: {e}")
    return True
