from django.db import models
from django.contrib.auth.models import User


from django.dispatch import receiver
from django.db.models.signals import post_save
# Create your models here.

def custom_upload_to(instance, filename):
    old_instance = userProfile.objects.get(pk=instance.pk)
    old_instance.imagen.delete()
    return 'profiles/' + filename

class userProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profi")
    imagen = models.ImageField(upload_to = custom_upload_to, null=True, blank=True)

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def ensure_profile_exists(sender, instance, **kwargs):
    if kwargs.get('created', False):
        userProfile.objects.get_or_create(user=instance)
#Se acaba de crear un usuario y su perfil enlazado, junto para resolver social
