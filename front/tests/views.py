from django.http import HttpResponse
try:
    from django.template import engines, RequestContext
    __is_18 = True
except ImportError:
    from django.template import RequestContext, loader
    __is_18 = False


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
        <div id="locale-ph">{% front_edit "locale-ph" request.LANGUAGE_CODE %}locale base content{% end_front_edit %}</div>
        <div id="some-other-ph">{% front_edit "some-other-ph" arg1 %}argument based content{% end_front_edit %}</div>
        {% front_edit_scripts editor="ace" %}
    </body>
</html>
'''


TEST_TEMPLATE_INVALID_EDITOR = r'''
{% load url from future %}
{% load front_tags %}
{% front_edit_scripts editor="dummy" %}
'''


def _get_template(template_string):
    if __is_18:
        return engines['django'].from_string(template_string)
    else:
        return loader.get_template_from_string(template_string)


def test(request):
    return HttpResponse(_get_template(TEST_TEMPLATE).render(RequestContext(request, dict(arg1='hello'))))


def test_invalid_template_tag(request):
    return HttpResponse(_get_template(TEST_TEMPLATE_INVALID_EDITOR).render(RequestContext(request, dict())))
