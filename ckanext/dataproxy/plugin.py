import ckan.plugins as p
import ckan.plugins.toolkit as tk
from ckanext.dataproxy.logic.action.create import dataproxy_resource_create
from ckanext.dataproxy.logic.action.update import dataproxy_resource_update
from ckan.logic import _actions


class DataProxyPlugin(p.SingletonPlugin):
    p.implements(p.IActions)
    p.implements(p.IRoutes, inherit=True)
    p.implements(p.IResourceController)
    p.implements(p.IConfigurer)

    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        tk.add_template_directory(config, 'templates')
        # Add public folder for extra JS & CSS
        tk.add_public_directory(config, 'public')


    def before_show(self, resource_dict):
        if resource_dict.get('url_type') == 'dataproxy':
            #Mask dataproxy resources as datastore ones for recline to render
            resource_dict['datastore_active'] = True
        return resource_dict
        

    def get_actions(self):
        return {'resource_create': dataproxy_resource_create,
                'resource_update': dataproxy_resource_update}

    def before_map(self, map):
        #Override API mapping on controller level to intercept dataproxy calls
        search_ctrl = 'ckanext.dataproxy.controllers.search:SearchController'
        map.connect('dataproxy', '/api/3/action/datastore_search', controller=search_ctrl, action='search_action')
        return map
