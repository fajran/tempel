from datetime import datetime, timedelta

from django.db import models
from django.conf import settings

from tempel import utils

def default_edit_expires():
    return datetime.now() + timedelta(seconds=60*settings.TEMPEL_EDIT_AGE)

class Entry(models.Model):
    content = models.TextField()
    language = models.CharField(max_length=20,
                                choices=utils.get_languages())
    created = models.DateTimeField(default=datetime.now)
    active = models.BooleanField(default=True)

    edit_token = models.CharField(max_length=8, default=utils.create_token, null=True)
    edit_expires = models.DateTimeField(default=default_edit_expires, null=True)

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

    def done_editable(self):
        self.edit_token = None
        self.save()

    def is_editable(self, token):
        time_ok = self.edit_expires is not None and self.edit_expires >= datetime.now()
        token_ok = self.edit_token is not None and token == self.edit_token
        return time_ok and time_ok

    def __unicode__(self):
        return '<Entry: id=%s lang=%s>' % (self.id, self.language)

