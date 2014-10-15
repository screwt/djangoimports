# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ImportModel'
        db.create_table(u'django_imports_importmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=30)),
        ))
        db.send_create_signal(u'django_imports', ['ImportModel'])

        # Adding model 'ImportModelItem'
        db.create_table(u'django_imports_importmodelitem', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('import_model', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['django_imports.ImportModel'])),
            ('model_field', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'django_imports', ['ImportModelItem'])


    def backwards(self, orm):
        # Deleting model 'ImportModel'
        db.delete_table(u'django_imports_importmodel')

        # Deleting model 'ImportModelItem'
        db.delete_table(u'django_imports_importmodelitem')


    models = {
        u'django_imports.importmodel': {
            'Meta': {'object_name': 'ImportModel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'})
        },
        u'django_imports.importmodelitem': {
            'Meta': {'object_name': 'ImportModelItem'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'import_model': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['django_imports.ImportModel']"}),
            'model_field': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'order': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['django_imports']