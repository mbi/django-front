from django.db import models
from django.core.cache import cache
from django.dispatch import receiver
from django.db.models.signals import post_save
import hashlib
import six


class Placeholder(models.Model):
    key = models.CharField(max_length=40, primary_key=True, db_index=True)
    value = models.TextField(blank=True)

    def __unicode__(self):
        return self.value

    def cache_key(self):
        return "front-edit-%s" % self.key

    @classmethod
    def key_for(cls, name, *bits):
        return hashlib.new('sha1', six.text_type(name + ''.join([six.text_type(token) for token in bits])).encode('utf8')).hexdigest()

    @classmethod
    def copy_content(cls, name, source_bits, target_bits):
        source_key = cls.key_for(name, *source_bits)
        target_key = cls.key_for(name, *target_bits)

        source = cls.objects.filter(key=source_key)
        if source.exists():
            source = source.get()
            cls.objects.create(key=target_key, value=source.value)


class PlaceholderHistory(models.Model):
    placeholder = models.ForeignKey(Placeholder, related_name='history', on_delete=models.CASCADE)
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
