from django import template
from classytags.core import Tag, Options
from classytags.arguments import Argument, MultiValueArgument, KeywordArgument
from django.core.cache import cache
from django.core.urlresolvers import reverse
from ..models import Placeholder
from ..conf import settings as django_front_settings
import hashlib
import six


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
        hash_val = hashlib.new('sha1', six.text_type(name + ''.join([six.text_type(token) for token in extra_bits])).encode('utf8')).hexdigest()
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

        user = context.get('request', None) and context.get('request').user
        if django_front_settings.DJANGO_FRONT_PERMISSION(user):
            return '<div class="editable" id="%s">%s</div>' % (hash_val, six.text_type(val).strip())
        return val or ''


class FrontEditJS(Tag):
    name = 'front_edit_scripts'
    options = Options(
        KeywordArgument('editor', resolve=False, required=False, defaultkey='editor')
    )

    def render_tag(self, context, editor=''):
        static_url = context.get('STATIC_URL', '/static/')
        user = context.get('request', None) and context.get('request').user
        token = six.text_type(context.get('csrf_token'))
        plugin = editor.get('editor').lower() if \
            editor.get('editor') and editor.get('editor').lower() \
            in ['ace', 'wymeditor', 'redactor'] else ''
        edit_mode = django_front_settings.DJANGO_FRONT_EDIT_MODE if \
            django_front_settings.DJANGO_FRONT_EDIT_MODE in ('lightbox', 'inline') else 'lightbox'

        if django_front_settings.DJANGO_FRONT_PERMISSION(user):
            return """
<link rel="stylesheet" href="%sfront/css/front-edit.css" />
<script>
    document._front_edit = {
        save_url: '%s',
        csrf_token: '%s',
        plugin: '%s',
        static_root: '%s',
        edit_mode: '%s'
    };
</script>
<script src="%sfront/js/front-edit.js"></script>""".strip() % (
                static_url,
                reverse('front-placeholder-save'),
                token,
                plugin,
                static_url,
                edit_mode,
                static_url
            )
        else:
            return ''


register.tag(FrontEditTag)
register.tag(FrontEditJS)
