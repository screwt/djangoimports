# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'ImportModelItem.selected'
        db.add_column(u'django_imports_importmodelitem', 'selected',
                      self.gf('django.db.models.fields.BooleanField')(default=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'ImportModelItem.selected'
        db.delete_column(u'django_imports_importmodelitem', 'selected')


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
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'selected': ('django.db.models.fields.BooleanField', [], {})
        }
    }

    complete_apps = ['django_imports']