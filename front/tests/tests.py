# -*- coding: utf-8 -*-
from front.models import Placeholder
from django.core.urlresolvers import reverse
from django.test import TestCase
from django.contrib.auth.models import User
from django.core.exceptions import ImproperlyConfigured
import re
import six
from django.core.cache import cache


class FrontTestCase(TestCase):

    urls = 'front.tests.urls'

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
