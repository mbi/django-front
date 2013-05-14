from .models import Placeholder
from django.http import HttpResponse
from .conf import settings as django_front_settings


def do_save(request):
    if request.POST and django_front_settings.DJANGO_FRONT_PERMISSION(request.user):
        key, val = request.POST.get('key'), request.POST.get('val')
        placeholder, _ = Placeholder.objects.get_or_create(key=key)
        placeholder.value = val
        placeholder.save()

        return HttpResponse('1')
    return HttpResponse('0')
