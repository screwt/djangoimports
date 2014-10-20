from django.shortcuts import render
from django.shortcuts import render_to_response,redirect
from django_imports.models import ImportModel, ImportModelItem
from django.http import HttpResponse
from pprint import pprint
from django.utils import simplejson
from django.conf import settings
from django.db.models import get_app, get_models
from django.core.exceptions import ImproperlyConfigured
from django.core.context_processors import csrf
from django import forms


class UploadFileForm(forms.Form):
    file = forms.FileField()

def get_model(fullname):
    appname = fullname.split(".")[:-1]
    appname = "".join(appname)
    modelname = fullname.split(".")[-1:]
    modelname = "".join(modelname)

    #print(appname,modelname)
    app = get_app(appname)
    result = None
    for model in get_models(app):
        #print(model,model._meta.object_name)
        if model._meta.object_name == modelname:
            result = model
            break
    return model

def get_available_models():
    apps = settings.INSTALLED_APPS
    model_list = []
    apps += ('auth',);
    for appname in apps:
        try:
            app = get_app(appname)
            for model in get_models(app):
                #pprint(dir(model._meta))
                #print("#####",model._meta.module_name,model._meta.object_name)
                mod = {"str":"{mod}.{obj}".format(mod=appname,obj=str(model._meta.object_name)),
                       "class":model,
                       "fields":[]}
                for f in model._meta.fields:
                    #if hasattr(f,'dir'):
                        #print(dir(f))
                    my_f = {}
                    if f.rel != None  and hasattr(f.rel,'get_related_field'):
                        #print(dir(f.rel.get_related_field()))
                        print(f.rel.get_related_field().model)
                        #for sub_f in f.rel.get_related_field():
                        #    print(str(f)+"    "+str(f))
                        print(dir(f.rel),f.rel.multiple)
                        many = 'false'
                        if f.rel.multiple:
                            many = "true"
                        my_f = {"name":f.name,
                                "is_related":"true",
                                'related_mod':"{mod}.{obj}".format(mod=f.rel.get_related_field().model._meta.app_label,obj=f.rel.get_related_field().model._meta.object_name),
                                'many':many}
                    else:
                        my_f = {"name":f.name,"is_related":"false","related_mod":'null','many':'false'}
                    mod["fields"].append(my_f)
                model_list.append(mod)
        except ImproperlyConfigured as e:
            pass
    #pprint(model_list)
    return model_list

#-- ImportModel creation/updating form
def import_model_form(request,pk=None,errs=None):
    UFileform = UploadFileForm(request.POST, request.FILES)
    c= {"pk":pk,"fileform":UFileform}

    if errs != None:
        errors_str = []
        for err in errs:
            errors_str.append(str(err))
        c.update({"errors":errors_str})

    if pk == None:
        #-- retrives avilable models
        mods = get_available_models()
        c.update({"model_list":mods})
    else:
        model = ImportModel.objects.get(pk=pk)
        model_items = ImportModelItem.objects.filter(import_model=model).order_by('order')
        
        c.update({'model':model,
                  'model_items':model_items})
    c.update(csrf(request))
    pprint(c)
    return render_to_response('import_model_form.html',c)

def import_model_push(request,pk=None):
    print("import_model_push",pk)
    #print(request.POST)
    #pprint(request.POST.items())
    refactored_data = {}
    cur_field = ""
    description = ""
    model = ""
    for key,value in request.POST.items():
        if key!="csrfmiddlewaretoken":
            if key=="description":
                description = value
            if key=="plugged_model":
                model = value
            if key.endswith("_field_name"):
                pass
            elif key.endswith("_selected"):
                if not refactored_data.has_key(key[:-9]):
                    refactored_data.update({key[:-9]:{}})
                refactored_data[key[:-9]].update({'selected':True})
            elif key.endswith("_position"):
                #print(key[:-9])
                if not refactored_data.has_key(key[:-9]):
                    refactored_data.update({key[:-9]:{}})
                refactored_data[key[:-9]].update({'position':value})

    for key,val in refactored_data.items():
        if not val.has_key("selected"):
            val.update({"selected":False})
            
    #print(description)
    pprint(refactored_data)
    
    im = ImportModel()
    if(pk!=None and pk!='None'):
        im = ImportModel.objects.get(pk=pk)
    im.name = description
    im.model_name = model
    im.save()

    #-- delete the old items
    oldIm = ImportModelItem.objects.filter(import_model=im)
    if(oldIm):
        oldIm.delete()

    for key,val in refactored_data.items():
        imi = ImportModelItem()
        imi.import_model = im
        imi.model_field = key
        imi.order= val["position"]
        imi.selected = val["selected"]
        imi.save()

    return redirect(import_model_form,pk=im.id)

#-- ImportModel list
def import_model_list(request):
    models = ImportModel.objects.all()
    return render_to_response('import_model_list.html',{'models':models})

#-- def model data
def get_model_data(resquest,mod):
    print(mod)
    data = {'fields':[],
            'app':''}
    #-- get desired model data
    return HttpResponse(simplejson.dumps(data), mimetype='application/json')
    


#-- export
def run_extract(request,pk):
    print(pk)
    #-- load parametred model
    parametred_model = ImportModel.objects.get(pk=pk)
    parametred_model_items = ImportModelItem.objects.filter(import_model=parametred_model).order_by('order')

    #-- try to query the model to extract
    mod = get_model(parametred_model.model_name)
    pprint(mod)
    data = list(mod.objects.all().values())
    pprint(data)

    out = ""

    #-- transform the query and select only values we want
    for instance in data:
        for item in parametred_model_items:
            if item.selected == True:
                #-- is it a related field
                if "." in item.model_field:
                    path = item.model_field.split(".")
                    if len(path)>2:
                        raise Exception("not yet implemented")
                    else:
                        if instance[path[0]+"_id"] is None:
                            out += u";"
                        else:
                            pprint(dir(instance))
                            out += u"{};".format(instance[path[0]+"_id"].__dict__[path[1]])
                else:
                    out += u"{};".format(instance[item.model_field])
        out += u"\n"

    return HttpResponse(out, mimetype='application/text')



#-- export
def run_import(request,pk):
    print("run_extract()",pk)

    #-- load parametred model
    parametred_model = ImportModel.objects.get(pk=pk)
    parametred_model_items = ImportModelItem.objects.filter(import_model=parametred_model,selected=True).order_by('order')

    #-- try to query the model to extract
    mod = get_model(parametred_model.model_name)

    #-- is a file present in the post data
    my_file = request.FILES['file']
    line_number = 0
    errors = []

    #-- read the file
    for line in my_file:
        line_number += 1
        #print(line[:-1])
        fields = line[:-1].split(";")
        #pprint(fields)
        tmp_dict = {}
        i = 0
        
        
        try :
            #-- verif format
            if len(fields) != len(parametred_model_items):
                raise Exception("Column number should be {}, your file contains {} columns see line {}".format(len(parametred_model_items),len(fields),line_number))
        
            for field in fields:
                tmp_dict.update({parametred_model_items[i].model_field:field})
                i+=1
                pprint(tmp_dict)

            #-- check if the instance already exists


            o = mod.objects.create(**tmp_dict)

            #-- save or update it
            o.save()
        except Exception as e:
            print("Error",e)
            errors.append({'msg':e,'line':line,'linenumber':line_number})
    c = {'errors':errors,'pk':pk}
    return render_to_response('import_model_report.html',c)
