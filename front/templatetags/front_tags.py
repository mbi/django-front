import json

from django import template
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.urls import NoReverseMatch, reverse  # NOQA
from django.utils.encoding import smart_str
from django.utils.html import strip_tags

import six
from classytags.arguments import Argument, KeywordArgument, MultiValueArgument
from classytags.core import Options, Tag

from ..conf import settings as django_front_settings
from ..models import Placeholder


register = template.Library()


class FrontEditTag(Tag):
    name = 'front_edit'
    options = Options(
        Argument('name', resolve=False, required=True),
        MultiValueArgument('extra_bits', required=False, resolve=True),
        blocks=[('end_front_edit', 'nodelist')],
    )

    def render_tag(self, context, name, extra_bits, nodelist=None):
        hash_val = Placeholder.key_for(name, *extra_bits)
        cache_key = "front-edit-%s" % hash_val

        val = cache.get(cache_key)
        if val is None:
            try:
                val = Placeholder.objects.get(key=hash_val).value
                cache.set(cache_key, val, 3600 * 24)
            except Placeholder.DoesNotExist:
                pass

        if val is None and nodelist:
            val = nodelist.render(context)

        classes = ['editable']

        if getattr(django_front_settings, 'DJANGO_FRONT_EXTRA_CONTAINER_CLASSES', None):
            classes.append(
                six.text_type(django_front_settings.DJANGO_FRONT_EXTRA_CONTAINER_CLASSES)
            )

        user = context.get('request', None) and context.get('request').user
        if django_front_settings.DJANGO_FRONT_PERMISSION(user):
            render = six.text_type(smart_str(val)).strip()
            if not strip_tags(render).strip():
                classes.append('empty-editable')

            return '<div class="%s" id="%s">%s</div>' % (
                ' '.join(classes),
                hash_val,
                render,
            )
        return val or ''


class FrontEditJS(Tag):
    name = 'front_edit_scripts'
    options = Options(
        KeywordArgument('editor', resolve=False, required=False, defaultkey='editor')
    )

    def render_tag(self, context, editor=''):
        try:
            save_url = reverse('front-placeholder-save')
            history_url = reverse('front-placeholder-history', args=('0000',))
        except NoReverseMatch:
            raise ImproperlyConfigured(
                'You must add an urlconf entry for django-front to work, see: http://django-front.readthedocs.org/en/latest/installation.html'
            )

        static_url = context.get('STATIC_URL', '/static/')
        user = context.get('request', None) and context.get('request').user
        token = six.text_type(context.get('csrf_token'))
        plugin = (
            editor.get('editor').lower()
            if editor.get('editor')
            and editor.get('editor').lower()
            in django_front_settings.DJANGO_FRONT_ALLOWED_EDITORS
            else 'default'
        )
        edit_mode = (
            django_front_settings.DJANGO_FRONT_EDIT_MODE
            if django_front_settings.DJANGO_FRONT_EDIT_MODE in ('lightbox', 'inline')
            else 'lightbox'
        )

        if django_front_settings.DJANGO_FRONT_PERMISSION(user):
            return """
<link rel="stylesheet" href="%sfront/css/front-edit.css" />
<script>
    document._front_edit = {
        save_url: '%s',
        history_url_prefix: '%s',
        csrf_token: '%s',
        plugin: '%s',
        static_root: '%s',
        edit_mode: '%s',
        editor_options: %s
    };
</script>
<script src="%sfront/js/front-edit.%s.js"></script>
<script src="%sfront/js/front-edit.js"></script>""".strip() % (
                static_url,
                save_url,
                history_url.replace('0000/', ''),
                token,
                plugin,
                static_url,
                edit_mode,
                json.dumps(django_front_settings.DJANGO_FRONT_EDITOR_OPTIONS),
                static_url,
                plugin,
                static_url,
            )
        else:
            return ''


register.tag(FrontEditTag)
register.tag(FrontEditJS)
