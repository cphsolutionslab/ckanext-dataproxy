import ckan.plugins as p
import ckan.plugins.toolkit as tk
from ckanext.dataproxy.logic.action.create import dataproxy_resource_create
from ckanext.dataproxy.logic.action.update import dataproxy_resource_update
#from ckanext.dataproxy.logic.action.action import dataproxy_datastore_search
from ckan.logic import _actions


class DataProxyPlugin(p.SingletonPlugin):
    p.implements(p.IActions)
    p.implements(p.IRoutes, inherit=True)
    p.implements(p.IResourceController, inherit=True)
    p.implements(p.IConfigurer)

    def update_config(self, config):
        # Add this plugin's templates dir to CKAN's extra_template_paths, so
        # that CKAN will use this plugin's custom templates.
        tk.add_template_directory(config, 'templates')
        # Add fanstatic folder for serving JS & CSS
        tk.add_resource('fanstatic', 'dataproxy')

    #2.3
    #def before_create(self, context, resource):
        #print('before create')
        #pass

    #def before_update(self, mapper, connection, instance):
        #print('before update')
        #pass

    #def after_update(self, context, pkg_dict):
        #print('after update')
        #pass

    #def after_create(self, context, pkg_dict):
        #print('after update')
        #pass
    
    #2.3 end

    def before_show(self, resource_dict):
        #print(resource_dict)
        if resource_dict.get('url_type') == 'dataproxy':
            #Mask dataproxy resources as datastore ones for recline to render
            print('datastore activated!')
            resource_dict['datastore_active'] = True
        return resource_dict
        

    def get_actions(self):
        return {'resource_create': dataproxy_resource_create,
                'resource_update': dataproxy_resource_update}
                #'datastore_search': dataproxy_datastore_search}

    def before_map(self, map):
        #Override API mapping on controller level to intercept dataproxy calls
        search_ctrl = 'ckanext.dataproxy.controllers.search:SearchController'
        map.connect('dataproxy', '/api/3/action/datastore_search', controller=search_ctrl, action='search_action')
        return map
