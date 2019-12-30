from django.shortcuts import render
from django.template import RequestContext


def home(request):
    return render(request, 'base.html')

def ace(request):
    return render(request, 'ace.html')

def epic(request):
    return render(request, 'epic.html')

def WYMeditor(request):
    return render(request, 'WYMeditor.html')
