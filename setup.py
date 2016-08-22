from setuptools import setup, find_packages


version = '0.2.0'
setup(
    name='ckanext-dataproxy',
    version=version,
    description="Proxy data from external databases",
    long_description='''
    ''',
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='',
    author='Fadeit Aps',
    author_email='ja@fadeit.dk',
    url='https://github.com/cphsolutionslab/ckanext-dataproxy',
    license='',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=['ckanext', 'ckanext.dataproxy'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # -*- Extra requirements: -*-
    ],
    entry_points='''
        [ckan.plugins]
        dataproxy=ckanext.dataproxy.plugin:DataproxyPlugin
        dataproxy_view=ckanext.dataproxy.plugin:DataproxyView
    ''',
)
