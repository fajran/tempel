from datetime import datetime, timedelta

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.core.urlresolvers import reverse

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from tempel.forms import EntryForm
from tempel.models import Entry
from tempel import utils

def index(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = Entry()
            entry.ip = request.META['REMOTE_ADDR']
            entry.content = form.cleaned_data['content']
            entry.language = form.cleaned_data['language']
            entry.save()

            age = 60 * settings.TEMPEL_EDIT_AGE
            path = reverse('tempel_view', args=[entry.id])

            response = HttpResponse(status=302)
            response['Location'] = path
            response.set_cookie('token', entry.edit_token, max_age=age, path=path)

            return response

    else:
        form = EntryForm()

    return render_to_response('index.html', {'form': form})

def edit(request, id, token):
    entry = get_object_or_404(Entry, pk=int(id))
    if not entry.active:
        raise Http404()

    if not entry.is_editable(token):
        return HttpResponse(status=403)

    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry.language = form.cleaned_data['language']
            entry.content = form.cleaned_data['content']
            entry.save()

            return HttpResponseRedirect(reverse('tempel_view', args=[entry.id]))
    else:
        data = {'language': entry.language,
                'content': entry.content}
        form = EntryForm(data)

    return render_to_response('edit.html', {'form': form})

def _view(request, id, mode='html', private_token=None):
    entry = get_object_or_404(Entry, pk=int(id))

    if not entry.active:
        raise Http404()

    if request.GET.has_key('download'):
        return HttpResponseRedirect(reverse('tempel_download', args=[entry.id]))

    edit_token = request.COOKIES.get('token', None)
    editable = entry.is_editable(edit_token)
    if not editable and entry.edit_token is not None:
        entry.done_editable()

    data = {'entry': entry,
            'language': entry.get_language(),
            'editable': editable,
            'token': edit_token}

    if mode == 'txt':
        ct = 'text/plain'
    else:
        ct = 'text/html'
        data['content'] = highlight(entry.content,
                                    get_lexer_by_name(entry.language),
                                    HtmlFormatter(linenos=True))

    return render_to_response('view.%s' % mode,
                              data, mimetype=ct)

def view(request, id, mode='html'):
    return _view(request, id, mode, None)

def _download(request, id, private_token=None):
    entry = get_object_or_404(Entry, pk=int(id))

    if not entry.active:
        raise Http404()

    data = {'entry': entry,
            'language': entry.get_language()}

    response = HttpResponse(entry.content)
    response['Content-Disposition'] = 'attachment; filename=%s' % \
                                        entry.get_filename()
    response['Content-Type'] = entry.get_mimetype()

    return response

def download(request, id):
    return _download(request, id, None)

