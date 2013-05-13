from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext


def home(request):
    return render_to_response('base.html', dict(
    ), context_instance=RequestContext(request))
