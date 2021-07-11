from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Slice(models.Model):
    top = models.CharField(max_length=255)
    middle = models.CharField(max_length=255)
    bottom = models.CharField(max_length=255)
    upload_date = models.DateField()
    is_public = models.BooleanField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Sandwich(models.Model):
    top = models.ForeignKey(Slice, on_delete=models.CASCADE)
    middle = models.ForeignKey(Slice, on_delete=models.CASCADE)
    bottom = models.ForeignKey(Slice, on_delete=models.CASCADE)
    creation_date = models.DateField()
    recent_update = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # included this in case you wanted to view the sandwich
    # in a dedicated detail page
    def get_absolute_url(self):
        return reverse('sandwich_detail', kwargs={'pk': self.id})
