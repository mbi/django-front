from .models import Placeholder
from django.http import HttpResponse


def do_save(request):
    if request.POST and request.user.is_staff:
        key, val = request.POST.get('key'), request.POST.get('val')
        placeholder, _ = Placeholder.objects.get_or_create(key=key)
        placeholder.value = val
        placeholder.save()

        return HttpResponse('1')
    return HttpResponse('0')
