from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': settings.MEDIA_ROOT}),
    (r'^admin/', include(admin.site.urls)),
    (r'^(?P<id>\d+)$', 'tempel.views.view', {'mode': 'html'}),
    (r'^(?P<id>\d+).html$', 'tempel.views.view', {'mode': 'html'}),
    (r'^(?P<id>\d+).txt$', 'tempel.views.view', {'mode': 'txt'}),
    (r'^$', 'tempel.views.index'),
)

