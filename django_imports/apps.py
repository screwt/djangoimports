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
