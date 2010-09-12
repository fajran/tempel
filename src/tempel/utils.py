import uuid
from datetime import datetime

from django.conf import settings

languages = dict([(item['name'], item) for item in settings.TEMPEL_LANGUAGES])

def get_languages():
    return sorted([(item['name'], item['label'])
                    for item in languages.values()])

def get_language(name):
    return languages[name]['label']

def get_mimetype(name):
    return languages[name]['mime']

def get_extension(name):
    return languages[name]['ext']

def create_token():
    return str(uuid.uuid4()).split('-')[0]

def is_editable(entry, token):
    from tempel.models import EditToken

    try:
        edit = EditToken.objects.get(entry=entry)
        if token is None:
            edit.delete()
        elif edit.expires < datetime.now():
            edit.delete()
        else:
            return True
        return False
    except EditToken.DoesNotExist:
        return False

