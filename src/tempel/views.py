from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.conf import settings
from django.core.urlresolvers import reverse

from pygments import highlight
from pygments.lexers import get_lexer_by_name
from pygments.formatters import HtmlFormatter

from tempel.forms import EntryForm
from tempel.models import Entry

def index(request):
    if request.method == 'POST':
        form = EntryForm(request.POST)
        if form.is_valid():
            entry = Entry()
            entry.content = form.cleaned_data['content']
            entry.language = form.cleaned_data['language']
            entry.save()

            return HttpResponseRedirect(reverse('tempel_view', args=[entry.id]))

    else:
        form = EntryForm()

    return render_to_response('index.html', {'form': form})

def view(request, id, mode='html'):
    entry = get_object_or_404(Entry, pk=int(id))

    if not entry.active:
        raise Http404()

    data = {'entry': entry,
            'language': entry.get_language()}

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

