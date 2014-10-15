from django.db import models
from django.contrib import admin

class ImportModel(models.Model):
    name = models.CharField(max_length=30)
    model_name = models.CharField(max_length=30)

admin.site.register(ImportModel)

class ImportModelItem(models.Model):
    import_model = models.ForeignKey(ImportModel)
    model_field = models.CharField(max_length=30)
    order = models.IntegerField()
    selected = models.BooleanField()

admin.site.register(ImportModelItem)    
