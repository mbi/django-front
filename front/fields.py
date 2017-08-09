from uuid import uuid4

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

from .models import Placeholder


class PlaceholderObject(object):
    def __init__(self, id, ph):
        self.ph = ph
        self.id = id


class PlaceholderField(models.UUIDField):
    def __init__(self, verbose_name=None, **kwargs):
        kwargs['null'] = True
        kwargs['default'] = None
        super().__init__(verbose_name, **kwargs)

    def get_db_prep_save(self, value, connection):
        if value is None:
            value = uuid4()
        return super().get_db_prep_save(value, connection)

    def from_db_value(self, value, expression, connection, context):
        ph = None
        try:
            ph = Placeholder.objects.get(key=str(value))
        except ObjectDoesNotExist:
            pass
        return PlaceholderObject(str(value), ph)
