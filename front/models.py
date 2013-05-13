from django.db import models
from django.core.cache import cache


class Placeholder(models.Model):
    key = models.CharField(max_length=40, primary_key=True, db_index=True)
    value = models.TextField(blank=True)

    def __unicode__(self):
        return self.value

    def cache_key(self):
        return "front-edit-%s" % self.key

    def save(self, *args, **kwargs):
        super(Placeholder, self).save(*args, **kwargs)
        cache.delete(self.cache_key())
