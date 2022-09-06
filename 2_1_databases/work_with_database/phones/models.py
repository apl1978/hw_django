from django.db import models
from django.urls import reverse


class Phone(models.Model):
    name = models.CharField(max_length= 200)
    price = models.IntegerField()
    image = models.CharField(max_length= 200)
    release_date = models.DateField()
    lte_exists = models.BooleanField()
    slug = models.SlugField(max_length = 200)

    def get_absolute_url(self):
        return reverse('phone', kwargs={'slug': self.slug})