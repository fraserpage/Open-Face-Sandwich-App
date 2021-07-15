from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Profile(models.Model):
    bio = models.TextField()
    img_src = models.CharField(max_length=255)
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Photo(models.Model):
    top = models.CharField(max_length=255)
    middle = models.CharField(max_length=255)
    bottom = models.CharField(max_length=255)
    upload_date = models.DateField(auto_now_add=True)
    is_public = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Sandwich(models.Model):
    top = models.ForeignKey(
        Photo, on_delete=models.CASCADE, related_name='top_id')
    middle = models.ForeignKey(
        Photo, on_delete=models.CASCADE, related_name='middle_id')
    bottom = models.ForeignKey(
        Photo, on_delete=models.CASCADE, related_name='bottom_id')
    creation_date = models.DateField(auto_now_add=True)
    recent_update = models.DateField(auto_now_add=True)
    thumbnail = models.TextField(default="thumbnail_url")
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # included this in case you wanted to view the sandwich
    # in a dedicated detail page
    def get_absolute_url(self):
        return reverse('sandwich_detail', kwargs={'pk': self.id})
