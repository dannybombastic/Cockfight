from django.db import models
from django.contrib.auth.models import User
from django.template import defaultfilters
from django.urls import reverse

#tags
from taggit.managers import TaggableManager


# Create your models here.
def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'recording/user_{0}/{1}'.format(instance.author, filename)

class Records(models.Model):
    title = models.CharField(max_length=60)
    descripcion = models.TextField(max_length=400, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.SET_NULL,
                                    related_name="get_records", null=True)
    upload = models.FileField(upload_to=user_directory_path)
    create = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    likes = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)
    slug = models.SlugField(max_length=60)
    tags = TaggableManager(
                    help_text="Ingresa tus HashTags, separados por coma.")

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = defaultfilters.slugify(self.title)
        super(Records, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("entradas:record_view", kwargs={'pk': self.pk, 'slug': self.slug})

    class Meta:
        ordering = ['-create']


class Comments(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    create = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(max_length=400)
    likes = models.PositiveIntegerField(default=0)
    status = models.BooleanField(default=True)
    recordOwn = models.ForeignKey(Records, related_name='get_comments',
                            on_delete=models.CASCADE)

    def __str__(self):
        return self.recordOwn.title

    class Meta:
        ordering = ['create']
