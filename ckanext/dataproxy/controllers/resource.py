from ckan.lib.base import model, abort, response, h, BaseController, request
import pylons.config as config
from ckan.controllers.package import PackageController
import ckan.logic as logic
import ckan.lib.navl.dictization_functions as dict_fns

clean_dict = logic.clean_dict
tuplize_dict = logic.tuplize_dict
parse_params = logic.parse_params



class ResourceController(PackageController):

    def new_resource(self, id, data=None, errors=None, error_summary=None):
        print('======================new_resource1============================')
        print(data)
        return super(ResourceController, self).new_resource(id, data, errors, error_summary)

    def resource_edit(self, id, resource_id, data=None, errors=None, error_summary=None):

        print('======================resource_edit============================')
        #data = data or clean_dict(dict_fns.unflatten(tuplize_dict(parse_params(request.POST))))
        #print(request.POST)
        #url_type = data.get('url_type', '')
        #if url_type == 'dataproxy':
            #secret = config.get('ckan.dataproxy.secret', False)
            #if not secret:
                #raise Exception('ckan.dataproxy.secret must be defined to encrypt passwords')
            #password = data['db_password']
            #connstr = data['url']
            #data['url'] = connstr.replace(password, '_password_')
            #data['db_password'] = encrypt(password, secret)
            #print('encrypted stuff')
            #print(data['db_password'])
            ##print('pw is:' + password)
            ##print('connstr is:' + connstr)
        #print(data)
        return super(ResourceController, self).resource_edit(id, resource_id, data, errors, error_summary)
