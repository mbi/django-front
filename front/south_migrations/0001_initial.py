# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Placeholder'
        db.create_table(u'front_placeholder', (
            ('key', self.gf('django.db.models.fields.CharField')(max_length=40, primary_key=True, db_index=True)),
            ('value', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal(u'front', ['Placeholder'])


    def backwards(self, orm):
        # Deleting model 'Placeholder'
        db.delete_table(u'front_placeholder')


    models = {
        u'front.placeholder': {
            'Meta': {'object_name': 'Placeholder'},
            'key': ('django.db.models.fields.CharField', [], {'max_length': '40', 'primary_key': 'True', 'db_index': 'True'}),
            'value': ('django.db.models.fields.TextField', [], {'blank': 'True'})
        }
    }

    complete_apps = ['front']