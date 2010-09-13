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

    url(r'^entry/(?P<id>\d+)/download/$', 'tempel.views.download', name='tempel_download'),
    url(r'^entry/(?P<id>\d+)/edit/(?P<token>\w{8})/$', 'tempel.views.edit', name='tempel_edit'),

    url(r'^(?P<id>\d+).(?P<private_token>\w{8})$', 'tempel.views.private_view', {'mode': 'html'}, name='tempel_private_view'),
    url(r'^(?P<id>\d+).(?P<private_token>\w{8}).html$', 'tempel.views.private_view', {'mode': 'html'}, name='tempel_private_html'),
    url(r'^(?P<id>\d+).(?P<private_token>\w{8}).txt$', 'tempel.views.private_view', {'mode': 'txt'}, name='tempel_private_raw'),

    url(r'^entry/(?P<id>\d+).(?P<private_token>\w{8})/download/$', 'tempel.views.private_download', name='tempel_private_download'),
    url(r'^entry/(?P<id>\d+).(?P<private_token>\w{8})/edit/(?P<token>\w{8})/$', 'tempel.views.private_edit', name='tempel_private_edit'),

    url(r'^$', 'tempel.views.index', name='tempel_index'),
)

