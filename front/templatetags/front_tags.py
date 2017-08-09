import six
from classytags.arguments import Argument, MultiValueArgument, KeywordArgument
from classytags.core import Tag, Options
from django import template
from django.conf import settings
from django.contrib.auth import get_permission_codename
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.encoding import smart_text
from django.utils.html import strip_tags

from ..conf import settings as django_front_settings
from ..models import Placeholder

try:
    import simplejson as json
except ImportError:
    import json

register = template.Library()


class FrontEditTag(Tag):
    name = 'front_edit'
    options = Options(
        Argument('name', resolve=False, required=True),
        MultiValueArgument('extra_bits', required=False, resolve=True),
        blocks=[
            ('end_front_edit', 'nodelist'),
        ]
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

        user = context.get('request', None) and context.get('request').user

        if django_front_settings.DJANGO_FRONT_PERMISSION(user):
            render = six.text_type(smart_text(val)).strip()
            if not strip_tags(render).strip():
                classes.append('empty-editable')

            return '<div class="%s" id="%s">%s</div>' % (' '.join(classes), hash_val, render)
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
                'You must add an urlconf entry for django-front to work, see: http://django-front.readthedocs.org/en/latest/installation.html')

        static_url = settings.STATIC_URL
        user = context.get('request', None) and context.get('request').user
        token = six.text_type(context.get('csrf_token'))
        plugin = editor.get('editor').lower() if editor.get('editor') and editor.get(
            'editor').lower() in django_front_settings.DJANGO_FRONT_ALLOWED_EDITORS else 'default'
        edit_mode = django_front_settings.DJANGO_FRONT_EDIT_MODE if django_front_settings.DJANGO_FRONT_EDIT_MODE in (
            'lightbox', 'inline') else 'lightbox'

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
        editor_options: %s,
        ucc: '',
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


class FrontEditModelTag(Tag):
    name = 'front_edit_model'
    options = Options(
        Argument('instance', resolve=False, required=True),
        blocks=[
            ('end_front_edit_model', 'nodelist'),
        ]
    )

    def render_tag(self, context, instance='', nodelist=None):
        obj = context.get('object', None)
        model_placeholder = getattr(obj, instance)
        hash_val = Placeholder.key_for(str(model_placeholder.id))
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

        user = context.get('request', None) and context.get('request').user

        user_can_change = False
        if obj:
            opts = type(obj)._meta
            codename = get_permission_codename('change', opts)
            change_perm = '{}.{}'.format(opts.app_label, codename)
            user_can_change = user.has_perm(change_perm)

        if django_front_settings.DJANGO_FRONT_PERMISSION(user) or user_can_change:
            render = six.text_type(smart_text(val)).strip()
            if not strip_tags(render).strip():
                classes.append('empty-editable')

            return '<div class="%s" id="%s">%s</div>' % (' '.join(classes), hash_val, render)
        return val or ''


class FrontEditModelJS(Tag):
    name = 'front_edit_model_scripts'
    options = Options(
        KeywordArgument('editor', resolve=False, required=False, defaultkey='editor')
    )

    def render_tag(self, context, editor=''):
        try:
            save_url = reverse('front-placeholder-save')
            history_url = reverse('front-placeholder-history', args=('0000',))
        except NoReverseMatch:
            raise ImproperlyConfigured(
                'You must add an urlconf entry for django-front to work, see: http://django-front.readthedocs.org/en/latest/installation.html')

        static_url = settings.STATIC_URL
        user = context.get('request', None) and context.get('request').user
        token = six.text_type(context.get('csrf_token'))
        plugin = editor.get('editor').lower() if editor.get('editor') and editor.get(
            'editor').lower() in django_front_settings.DJANGO_FRONT_ALLOWED_EDITORS else 'default'
        edit_mode = django_front_settings.DJANGO_FRONT_EDIT_MODE if django_front_settings.DJANGO_FRONT_EDIT_MODE in (
            'lightbox', 'inline') else 'lightbox'

        obj = context.get('object', None)
        user_can_change = False
        if obj:
            opts = type(obj)._meta
            codename = get_permission_codename('change', opts)
            change_perm = '{}.{}'.format(opts.app_label, codename)
            user_can_change = user.has_perm(change_perm)

        if obj and django_front_settings.DJANGO_FRONT_PERMISSION(user) or user_can_change:
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
        editor_options: %s,
        ucc: '%s',
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
                user_can_change,
                static_url,
                plugin,
                static_url,
            )
        else:
            return ''


register.tag(FrontEditTag)
register.tag(FrontEditModelTag)
register.tag(FrontEditJS)
register.tag(FrontEditModelJS)
