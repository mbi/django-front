# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PlaceholderHistory'
        db.create_table(u'front_placeholderhistory', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('placeholder', self.gf('django.db.models.fields.related.ForeignKey')(related_name='history', to=orm['front.Placeholder'])),
            ('value', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('saved', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
        ))
        db.send_create_signal(u'front', ['PlaceholderHistory'])


    def backwards(self, orm):
        # Deleting model 'PlaceholderHistory'
        db.delete_table(u'front_placeholderhistory')


    models = {
        u'front.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True', 'db_index': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        },
        u'front.placeholderhistory': {
            'Meta': {'object_name': 'PlaceholderHistory'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'placeholder': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'history'", 'to': u"orm['front.Placeholder']"}),
            'saved': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['front']