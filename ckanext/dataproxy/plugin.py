from ckan import __version__
import json
import ckan.plugins as p
import ckan.plugins.toolkit as tk
from ckanext.dataproxy.logic.action.create import dataproxy_resource_create
from ckanext.dataproxy.logic.action.update import dataproxy_resource_update

# When __version__ is a patch release like '2.3.1'
# or worse, '2.3.1b', get the minor point release.
minor   = '.'.join(__version__.split('.')[0:2]) #=> '2.3'
version = float(minor)

if version >= 2.3:
    from ckanext.reclineview.plugin import ReclineViewBase
    from ckan.lib.helpers import resource_view_get_fields

    def resource_view_get_fields_override(resource):
        #Skip filter fields lookup for dataproxy resources
        if resource.get('url_type', '') == 'dataproxy':
            return []
        return resource_view_get_fields(resource)
    
    class DataBaseProxyView(ReclineViewBase):
        p.implements(p.ITemplateHelpers)
    
        def get_helpers(self):
            return {'resource_view_get_fields': resource_view_get_fields_override}
    
        def info(self):
            ''' IResourceView '''
            return {'name': 'database_proxy_view',
                    'title': p.toolkit._('Database Proxy Explorer'),
                    'icon': 'table',
                    'default_title': p.toolkit._('Database Proxy Explorer'),
                    }
    
        def can_view(self, data_dict):
            ''' IResourceView '''
            resource = data_dict['resource']
            return resource.get('url_type', '') == 'dataproxy'
    
        def setup_template_variables(self, context, data_dict):
            #Instead of masking the resource as in < 2.3, we add datastore_active as json value
            #So recline would request datastore api endpoint, but ckan itself knows it's not datastore
            #therefore ckan won't offer recline views to dataproxy resources
            data_dict['resource']['datastore_active'] = True
            return {'resource_json': json.dumps(data_dict['resource']),
                     'resource_view_json': json.dumps(data_dict['resource_view'])}
    

class DataProxyPlugin(p.SingletonPlugin):
    p.implements(p.IActions)
    p.implements(p.IConfigurer)
    p.implements(p.IRoutes, inherit=True)
    p.implements(p.IResourceController, inherit=True)
    
    def before_show(self, resource_dict):
        ''' IResourceController '''
        if 'db_password' in resource_dict:
            #Remove db_password from display fields (although it's encrypted)
            resource_dict.pop('db_password')
        if version < 2.3:
            #For versions below 2.3 we mask dataproxy resources as datastore ones
            if resource_dict.get('url_type') == 'dataproxy':
                resource_dict['datastore_active'] = True
        return resource_dict
    
    def update_config(self, config):
        ''' IConfigurer '''
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        tk.add_template_directory(config, 'templates')
        # Add fanstatic folder for serving JS & CSS
        tk.add_resource('fanstatic', 'dataproxy')

    def get_actions(self):
        ''' IActions '''
        return {'resource_create': dataproxy_resource_create,
                'resource_update': dataproxy_resource_update}

    def before_map(self, map):
        ''' IRoutes '''
        #Override API mapping on controller level to intercept dataproxy calls
        search_ctrl = 'ckanext.dataproxy.controllers.search:SearchController'
        map.connect('dataproxy', '/api/3/action/datastore_search', controller=search_ctrl, action='search_action')
        map.connect('dataproxy', '/api/3/action/datastore_search_sql', controller=search_ctrl, action='search_sql_action')
        return map
