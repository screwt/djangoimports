from setuptools import setup,find_packages

setup(
    name='django-imports',
    version='0.1',
    packages = find_packages(),
    package_data = {
        # If any package contains *.txt or *.rst files, include them:
        '': ['*.py', '*.html'],
    },
    include_package_data=True,
    license='GPLv2 License',  # example license
    description='Description',
    long_description="Long descr",
    url='http://www.example.com/',
    author='Benoit Juin',
    author_email='benoit.juin@gmail.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GPLv2 License', # example license
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 2.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
)
