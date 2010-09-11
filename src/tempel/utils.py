from django.conf import settings

languages = dict([(item['name'], item) for item in settings.TEMPEL_LANGUAGES])

def get_languages():
    return sorted([(item['name'], item['label']) for item in languages.values()])

def get_language(name):
    return languages[name]['label']

def get_mimetype(name):
    return languages[name]['mime']

def get_extension(name):
    return languages[name]['ext']

