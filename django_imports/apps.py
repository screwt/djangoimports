 #-- django 1.7 ...
#from django.apps import AppConfig
#logger = logging.getLogger('console')
#class dcConfig(AppConfig):
#    name = 'django-imports'
#    verbose_name = "django csv file import module"


#    def ready(self):
#        print("test")
#        logger.debug("App django-imports ready")
        #autodiscover_modules('events')

from django_imports.views import import_model_form,\
                                 import_model_list,\
                                 get_model_data,\
                                 import_model_push,\
                                 run_extract,\
                                 run_import

from django.conf.urls import patterns, url, include

from django.conf import settings
from django.utils.importlib import import_module
import traceback
import sys


def urls():
    return patterns('',
                    url(r'^$',import_model_list),
                    url(r'^(?P<pk>\d+)$',import_model_form),
                    url(r'^create/$',import_model_form),
                    url(r'^push/(?P<pk>\w+)$',import_model_push),
                    url(r'^get_model_data/(?P<mod>\w+)/$',get_model_data),
                    url(r'^extract/(?P<pk>\d+)/$',run_extract),
                    url(r'^import/(?P<pk>\d+)/$',run_import),
                    )


class DISite(object):
    def __init__(self):
        self.registry = {}

    #-- register validator tool
    def register(self,model,fun):
        model_full_name = "{app}.{mod}".format(app=model._meta.app_label,mod=model._meta.object_name)
        #print("register()",model_full_name)
         
        if  model_full_name not in self.registry:
            self.registry.update({model_full_name:[]})
        #print(dir(fun))
        self.registry[model_full_name].append("{app}.{fun}".format(app=fun.__module__,fun=fun.func_name))
        print("register()",self.registry) 
    


di_site = DISite()

  
#-- initializer function
def initialize():
    #-- look for existing validators, DI_validators.py modules in any app
    #-- will be done in views in django <1.7 , the APPConfig.ready() function could be use in later versions
    for app in settings.INSTALLED_APPS:
        mod = import_module(app)
        try:
            import_module('%s.DI_validators' % app)
            print("Found DI_validators in %s" % app)
        except ImportError as e: 
            #print(e)
            #print traceback.format_exc()
            #print("No DI_validators in %s" % app)
            pass
    

