from django.conf.urls.defaults import *
from django.conf import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^\+media/(?P<path>.*)$', 'django.views.static.serve', 
        {'document_root': settings.MEDIA_ROOT}),
    (r'^admin/', include(admin.site.urls)),
    url(r'^(?P<id>\d+)$', 'tempel.views.view', {'mode': 'html'}, name='tempel_view'),
    url(r'^(?P<id>\d+).html$', 'tempel.views.view', {'mode': 'html'}, name='tempel_html'),
    url(r'^(?P<id>\d+).txt$', 'tempel.views.view', {'mode': 'txt'}, name='tempel_raw'),
    url(r'^e/(?P<id>\d+)/download/$', 'tempel.views.download', name='tempel_download'),
    url(r'^$', 'tempel.views.index', name='tempel_index'),
)

