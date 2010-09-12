from datetime import datetime, timedelta

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.core.urlresolvers import reverse

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from tempel.forms import EntryForm
from tempel.models import Entry, EditToken
from tempel import utils

def index(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = Entry()
            entry.content = form.cleaned_data['content']
            entry.language = form.cleaned_data['language']
            entry.save()

            token = utils.create_token()
            age = 60 * settings.TEMPEL_EDIT_AGE

            edit = EditToken()
            edit.entry = entry
            edit.token = token
            edit.expires = datetime.now() + timedelta(seconds=age)
            edit.save()

            path = reverse('tempel_view', args=[entry.id])

            response = HttpResponse(status=302)
            response['Location'] = path
            response.set_cookie('token', token, max_age=age, path=path)

            return response

    else:
        form = EntryForm()

    return render_to_response('index.html', {'form': form})

def edit(request, id, token):
    entry = get_object_or_404(Entry, pk=int(id))
    if not entry.active:
        raise Http404()

    editable = utils.is_editable(entry, token)
    print 'editable:', editable
    if not editable:
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

def view(request, id, mode='html'):
    entry = get_object_or_404(Entry, pk=int(id))

    if not entry.active:
        raise Http404()

    editable = utils.is_editable(entry, request.COOKIES.get('token', None))

    data = {'entry': entry,
            'language': entry.get_language(),
            'editable': editable,
            'token': request.COOKIES.get('token', None)}

    if mode == 'txt':
        ct = 'text/plain'
    else:
        ct = 'text/html'
        data['content'] = highlight(entry.content,
                                    get_lexer_by_name(entry.language),
                                    HtmlFormatter(linenos=True))

    return render_to_response('view.%s' % mode,
                              data, mimetype=ct)

def download(request, id):
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

