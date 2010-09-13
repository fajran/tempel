from datetime import datetime, timedelta

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.core.urlresolvers import reverse

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from tempel.forms import EntryForm, EditForm
from tempel.models import Entry
from tempel import utils

def _get_initial(entry_id):
    if entry_id is None:
        return {}

    id = None
    private_token = None

    p = entry_id.split('.')
    if len(p) >= 1:
        id = int(p[0])
    if len(p) >= 2:
        private_token = p[1]

    if id is None:
        return {}
    if private_token is not None and len(private_token) != 8:
        return {}

    try:
        entry = Entry.objects.get(pk=id, private_token=private_token)
        return {'content': entry.content,
                'language': entry.language,
                'private': private_token is not None}
    except Entry.DoesNotExist:
        return {}

def index(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            private = form.cleaned_data['private']

            entry = Entry()
            entry.ip = request.META['REMOTE_ADDR']
            entry.content = form.cleaned_data['content']
            entry.language = form.cleaned_data['language']
            if private:
                entry.private_token = utils.create_token()
            entry.save()

            age = 60 * settings.TEMPEL_EDIT_AGE
            path = entry.view_url()

            response = HttpResponse(status=302)
            response['Location'] = path
            response.set_cookie('token', entry.edit_token,
                                max_age=age, path=path)

            return response

    else:
        initial = _get_initial(request.GET.get('duplicate', None))
        form = EntryForm(initial)

    return render_to_response('index.html', {'form': form})

def _edit(request, id, token, private_token=None):
    entry = get_object_or_404(Entry, pk=int(id), private_token=private_token)
    if not entry.active:
        raise Http404()

    if not entry.is_editable(token):
        return HttpResponse(status=403)

    if request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            entry.language = form.cleaned_data['language']
            entry.content = form.cleaned_data['content']
            entry.save()

            return HttpResponseRedirect(entry.view_url())
    else:
        data = {'language': entry.language,
                'content': entry.content}
        form = EditForm(data)

    return render_to_response('edit.html', {'form': form})

def edit(request, id, token):
    return _edit(request, id, token, None)

def private_edit(request, id, private_token, token):
    return _edit(request, id, token, private_token)

def _view(request, id, mode='html', private_token=None):
    entry = get_object_or_404(Entry, pk=int(id), private_token=private_token)

    if not entry.active:
        raise Http404()

    if request.GET.has_key('download'):
        return HttpResponseRedirect(entry.download_url())

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

def private_view(request, id, private_token, mode='html'):
    return _view(request, id, mode, private_token)

def _download(request, id, private_token=None):
    entry = get_object_or_404(Entry, pk=int(id), private_token=private_token)

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

def private_download(request, id, private_token):
    return _download(request, id, private_token)

