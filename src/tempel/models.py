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

    def get_language(self):
        return utils.get_language(self.language)

    def get_mimetype(self):
        return utils.get_mimetype(self.language)

    def get_filename(self):
        return '%s.%s' % (self.id, self.get_extension())

    def get_extension(self):
        return utils.get_extension(self.language)

    def __unicode__(self):
        return '<Entry: id=%s lang=%s>' % (self.id, self.language)

