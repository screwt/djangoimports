default_app_config = 'django-imports.apps.dcConfig'
def autodiscover():
    """
    Auto-discover INSTALLED_APPS admin.py modules and fail silently when
    not present. This forces an import on them to register any admin bits they
    may want.
    """
    print("autodico")
