from django import forms
from django.template import RequestContext, loader
from django.http import HttpResponse


TEST_TEMPLATE = r'''
{% load url from future %}
{% load front_tags %}
<!DOCTYPE html>
<html lang="{{LANGUAGE_CODE}}">
    <head>
        <meta http-equiv="Content-type" content="text/html; charset=utf-8">
        <title>front test</title>
    </head>
    <body>
        <p>Hello, {% if request.user.is_authenticated %}{{request.user}}{% else %}Anon{% endif %}!</p>
        <div id="global-ph">{% front_edit "global-ph" %}global base content{% end_front_edit  %}</div>
        <div id="locale-ph">{% front_edit "locale-ph" LANGUAGE_CODE %}locale base content{% end_front_edit  %}</div>
        {% front_edit_scripts editor="ace" %}
    </body>
</html>
'''

def test(request):
    t = loader.get_template_from_string(TEST_TEMPLATE)
    return HttpResponse(t.render(RequestContext(request, dict())))
