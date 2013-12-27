from django.db import models
from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save


class Placeholder(models.Model):
    key = models.CharField(max_length=40, primary_key=True, db_index=True)
    value = models.TextField(blank=True)

    def __unicode__(self):
        return self.value

    def cache_key(self):
        return "front-edit-%s" % self.key


class PlaceholderHistory(models.Model):
    placeholder = models.ForeignKey(Placeholder, related_name='history')
    value = models.TextField(blank=True)
    saved = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-saved', )

    @property
    def _as_json(self):
        return {'value': self.value, 'saved': self.saved.strftime('%s')}


@receiver(post_save, sender=Placeholder)
def save_placeholder(sender, instance, created, raw, *args, **kwargs):
    if not raw:
        # If we have placeholders, check wheter the content has changed before saving history
        if PlaceholderHistory.objects.filter(placeholder=instance).exists():
            ph = PlaceholderHistory.objects.all()[0]
            if ph.value != instance.value:
                PlaceholderHistory.objects.create(placeholder=instance, value=instance.value)
        else:
            PlaceholderHistory.objects.create(placeholder=instance, value=instance.value)


@receiver(post_save, sender=PlaceholderHistory)
def save_history(sender, instance, created, raw, *args, **kwargs):
    cache.delete(instance.placeholder.cache_key())
