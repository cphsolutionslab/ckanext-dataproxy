from ckan.logic import get_action
import pylons.config as config
from simplecrypt import encrypt
from binascii import hexlify
from ckan.model import Resource

orig_resource_update = get_action('resource_update')

def dataproxy_resource_update(context, data_dict=None):
    """
    Intercepts default resource_update action and encrypts password for dataproxy type resources
    Args:
        context: Request context.
        data_dict: Parsed request parameters.
    Returns:
        see get_action('resource_update').
    Raises:
        Exception: if ckan.dataproxy.secret configuration not set.
    """
    #If not set, default to empty string
    data_dict['url_type'] = data_dict.get('url_type', '')
    url_type = data_dict['url_type']

    if url_type == 'dataproxy':
        secret = config.get('ckan.dataproxy.secret', False)
        if not secret:
            raise Exception('ckan.dataproxy.secret must be defined to encrypt passwords')
        #replace password with a _password_ placeholder
        password = data_dict.get('db_password', '')
        if password == '':
            #we don't want to overwrite existing password with empty string
            resource = Resource.get(data_dict['id'])
            data_dict['db_password'] = resource.extras['db_password']
        else:
            data_dict['url'] = data_dict['url'].replace(password, '_password_')
            #encrypt db_password
            data_dict['db_password'] = hexlify(encrypt(secret, password))

    return orig_resource_update(context, data_dict)
