from django.db import models
from django.conf import settings

from tempel import utils

class Entry(models.Model):
    content = models.TextField()
    language = models.CharField(max_length=20,
                                choices=utils.get_languages())
    created = models.DateTimeField(auto_now=True, auto_now_add=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ['-created']
        verbose_name_plural = "entries"
        

