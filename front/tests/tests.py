# -*- coding: utf-8 -*-
import json
import re

import six
from django.contrib.auth.models import User
from django.core.cache import cache
from django.core.exceptions import ImproperlyConfigured
from django.test import TestCase, override_settings
from django.urls import reverse
from front.models import Placeholder, PlaceholderHistory
from front.conf import settings as django_front_settings


@override_settings(ROOT_URLCONF='front.tests.urls')
class FrontTestCase(TestCase):

    def setUp(self):
        self.admin_user = User.objects.create_user('admin_user', 'admin@admin.com', 'admin_user')
        self.admin_user.is_staff = True
        self.admin_user.is_superuser = True
        self.admin_user.save()

    def tearDown(self):
        cache.clear()

    def test_1_anonymous_user_cant_see_tags(self):
        resp = self.client.get(reverse('front-test'))
        self.assertTrue('document._front_edit' not in six.text_type(resp.content))

    def test_2_root_user_does(self):
        self.client.login(username='admin_user', password='admin_user')
        resp = self.client.get(reverse('front-test'))
        self.assertTrue('document._front_edit' in six.text_type(resp.content))
        self.assertTrue(six.text_type("plugin: 'ace'") in six.text_type(resp.content.decode('utf8')))

    def test_3_anonymous_user_cant_post_either(self):
        resp = self.client.post(reverse('front-placeholder-save'), {'key': '123123', 'val': '<p>booh!</p>'})
        self.assertTrue('0' in six.text_type(resp.content))
        self.assertEqual(0, Placeholder.objects.count())

    def test_4_but_admin_shall_post(self):
        self.client.login(username='admin_user', password='admin_user')
        resp = self.client.post(reverse('front-placeholder-save'), {'key': '123123', 'val': '<p>booh!</p>'})
        self.assertTrue('1' in six.text_type(resp.content))
        self.assertEqual(1, Placeholder.objects.count())

    def test_5_workflow_baby(self):
        self.client.login(username='admin_user', password='admin_user')
        resp = self.client.get(reverse('front-test'))
        ids = re.findall(r'<div class="editable" id="([^"]+)">', six.text_type(resp.content))
        self.assertTrue(len(ids))

        self.assertTrue('global base content' in six.text_type(resp.content))
        resp = self.client.post(reverse('front-placeholder-save'), {'key': ids[0], 'val': '<p>booh!</p>'})
        resp = self.client.post(reverse('front-placeholder-save'), {'key': ids[1], 'val': '<p>english!</p>'})

        resp = self.client.get(reverse('front-test'))
        self.assertFalse('global base content' in six.text_type(resp.content))
        self.assertTrue('booh!' in six.text_type(resp.content))
        self.assertTrue('english!' in six.text_type(resp.content))
        self.assertTrue('locale base content' not in six.text_type(resp.content))

        # Parlez vous francais?
        # The global placholder should display the same in english, but not the localized one
        self.client.post('/i18n/setlang/', {'language': 'fr'})
        resp = self.client.get(reverse('front-test'))
        self.assertFalse('global base content' in six.text_type(resp.content))
        self.assertTrue('booh!' in six.text_type(resp.content))
        self.assertFalse('english!' in six.text_type(resp.content))
        self.assertFalse('locale base content' not in six.text_type(resp.content))

    def test_6_warn_when_missing_urlconf(self):
        with self.settings(ROOT_URLCONF='front.tests.urls_no_save'):
            self.client.login(username='admin_user', password='admin_user')
            try:
                self.client.get(reverse('front-test'))
                self.fail()
            except ImproperlyConfigured:
                pass

    def test_7_empty_content(self):
        self.client.login(username='admin_user', password='admin_user')
        resp = self.client.get(reverse('front-test'))
        self.assertFalse('empty-editable' in six.text_type(resp.content))
        ids = re.findall(r'<div class="editable" id="([^"]+)">', six.text_type(resp.content))

        resp = self.client.post(reverse('front-placeholder-save'), {'key': ids[0], 'val': ''})
        self.assertTrue('1' in six.text_type(resp.content))
        resp = self.client.get(reverse('front-test'))
        self.assertTrue('empty-editable' in six.text_type(resp.content))

        resp = self.client.post(reverse('front-placeholder-save'), {'key': ids[0], 'val': '<p>    </p>'})
        self.assertTrue('1' in six.text_type(resp.content))
        resp = self.client.get(reverse('front-test'))
        self.assertTrue('empty-editable' in six.text_type(resp.content))

        resp = self.client.post(reverse('front-placeholder-save'), {'key': ids[0], 'val': '<p>booh</p>'})
        self.assertTrue('1' in six.text_type(resp.content))
        resp = self.client.get(reverse('front-test'))
        self.assertFalse('empty-editable' in six.text_type(resp.content))

    def test_8_save_history(self):
        self.assertEqual(0, PlaceholderHistory.objects.count())

        self.client.login(username='admin_user', password='admin_user')
        resp = self.client.get(reverse('front-test'))
        self.assertFalse('empty-editable' in six.text_type(resp.content))
        ids = re.findall(r'<div class="editable" id="([^"]+)">', six.text_type(resp.content))
        key = ids[0]

        resp = self.client.post(reverse('front-placeholder-save'), {'key': key, 'val': '<p>booh</p>'})
        self.assertTrue('1' in six.text_type(resp.content))
        resp = self.client.get(reverse('front-test'))

        self.assertEqual(1, PlaceholderHistory.objects.filter(placeholder__key=key).count())

        resp = self.client.post(reverse('front-placeholder-save'), {'key': key, 'val': '<p>booh, too</p>'})
        resp = self.client.get(reverse('front-test'))

        self.assertEqual(2, PlaceholderHistory.objects.filter(placeholder__key=key).count())

        resp = self.client.post(reverse('front-placeholder-save'), {'key': key, 'val': ''})
        self.assertEqual(3, PlaceholderHistory.objects.filter(placeholder__key=key).count())

    def test_9_get_history(self):
        self.client.login(username='admin_user', password='admin_user')
        resp = self.client.get(reverse('front-test'))
        self.assertFalse('empty-editable' in six.text_type(resp.content))
        ids = re.findall(r'<div class="editable" id="([^"]+)">', six.text_type(resp.content))
        key = ids[0]

        resp = self.client.post(reverse('front-placeholder-save'), {'key': key, 'val': '<p>booh</p>'})
        resp = self.client.post(reverse('front-placeholder-save'), {'key': key, 'val': '<p>booh, too</p>'})
        resp = self.client.post(reverse('front-placeholder-save'), {'key': key, 'val': ''})
        resp = self.client.post(reverse('front-placeholder-save'), {'key': key, 'val': u'<p>aéaéaàà</p>'})

        self.assertEqual(4, PlaceholderHistory.objects.filter(placeholder__key=key).count())

        resp = self.client.get(reverse('front-placeholder-history', args=(key, )))
        self.assertTrue('application/json' in resp['Content-Type'])

        self.assertTrue(u'<p>aéaéaàà</p>' in [ph.get('value') for ph in json.loads(resp.content.decode("utf8")).get('history')])

    def test_10_history_only_saves_changes(self):

        self.client.login(username='admin_user', password='admin_user')
        resp = self.client.get(reverse('front-test'))
        self.assertFalse('empty-editable' in six.text_type(resp.content))
        ids = re.findall(r'<div class="editable" id="([^"]+)">', six.text_type(resp.content))
        key = ids[0]

        resp = self.client.post(reverse('front-placeholder-save'), {'key': key, 'val': '<p>booh</p>'})
        resp = self.client.post(reverse('front-placeholder-save'), {'key': key, 'val': '<p>booh, too</p>'})

        self.assertEqual(2, PlaceholderHistory.objects.filter(placeholder__key=key).count())

        resp = self.client.post(reverse('front-placeholder-save'), {'key': key, 'val': '<p>booh, too</p>'})
        self.assertEqual(2, PlaceholderHistory.objects.filter(placeholder__key=key).count())

        resp = self.client.post(reverse('front-placeholder-save'), {'key': key, 'val': '<p>booh</p>'})
        self.assertEqual(3, PlaceholderHistory.objects.filter(placeholder__key=key).count())

        resp = self.client.post(reverse('front-placeholder-save'), {'key': key, 'val': '<p>booh</p>'})
        self.assertEqual(3, PlaceholderHistory.objects.filter(placeholder__key=key).count())

    def test_11_invalid_tag(self):
        self.client.login(username='admin_user', password='admin_user')
        resp = self.client.get(reverse('front-test_invalid_template_tag'))
        self.assertTrue(six.text_type(u"plugin: 'default'") in six.text_type(resp.content.decode('utf8')))

    def test_12_calculate_keys(self):
        self.client.login(username='admin_user', password='admin_user')
        resp = self.client.get(reverse('front-test'))
        self.assertFalse('empty-editable' in six.text_type(resp.content))
        ids = re.findall(r'<div class="editable" id="([^"]+)">', six.text_type(resp.content))
        self.assertEqual(six.text_type(ids[0]), six.text_type('d577f15230caa8d39fb651d5b1ea34743f56edff'))

    def test_13_copy_content(self):
        self.assertEqual(0, Placeholder.objects.count())
        self.client.login(username='admin_user', password='admin_user')

        resp = self.client.get(reverse('front-test'))
        key = Placeholder.key_for('global-ph')
        self.assertTrue(key in six.text_type(resp.content))
        key = Placeholder.key_for('some-other-ph', 'hello')
        self.assertTrue(key in six.text_type(resp.content))

        resp = self.client.post(reverse('front-placeholder-save'), {'key': key, 'val': '<p>booh</p>'})
        self.assertEqual(1, Placeholder.objects.count())

        Placeholder.copy_content('some-other-ph', ['hello'], ['jello'])
        self.assertEqual(2, Placeholder.objects.count())

        jello_key = Placeholder.key_for('some-other-ph', 'jello')
        hello_key = Placeholder.key_for('some-other-ph', 'hello')
        self.assertTrue(Placeholder.objects.filter(key=jello_key).exists())
        self.assertTrue(Placeholder.objects.filter(key=hello_key).exists())
        self.assertEqual(
            Placeholder.objects.get(key=jello_key).value,
            Placeholder.objects.get(key=jello_key).value
        )

    def test_14_extra_container_classes(self):
        _setting = getattr(django_front_settings, 'DJANGO_FRONT_EXTRA_CONTAINER_CLASSES', '')
        django_front_settings.DJANGO_FRONT_EXTRA_CONTAINER_CLASSES = 'some extra classes'

        self.client.login(username='admin_user', password='admin_user')
        resp = self.client.get(reverse('front-test'))
        self.assertTrue('some extra classes' in six.text_type(resp.content))

        django_front_settings.DJANGO_FRONT_EXTRA_CONTAINER_CLASSES = _setting
