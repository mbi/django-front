from .conf import settings as django_front_settings
from .models import Placeholder, PlaceholderHistory
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.views.decorators.http import require_POST, require_GET
import json


class JsonHttpResponse(HttpResponse):
    def __init__(self, **kwargs):
        super(JsonHttpResponse, self).__init__(json.dumps(kwargs, cls=DjangoJSONEncoder, ensure_ascii=False), content_type='application/json')


@require_POST
def do_save(request):
    if request.POST and django_front_settings.DJANGO_FRONT_PERMISSION(request.user):
        key, val = request.POST.get('key'), request.POST.get('val')
        placeholder, created = Placeholder.objects.get_or_create(key=key, defaults=dict(value=val))
        if not created:
            placeholder.value = val
            placeholder.save()

        return HttpResponse('1')
    return HttpResponse('0')


@require_GET
def get_history(request, key):
    return JsonHttpResponse(history=[ph._as_json for ph in PlaceholderHistory.objects.filter(placeholder__key=key)])
