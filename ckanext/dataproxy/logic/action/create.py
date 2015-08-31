from ckan.logic import get_action
import pylons.config as config
from simplecrypt import encrypt
from binascii import hexlify

orig_resource_create = get_action('resource_create')

def dataproxy_resource_create(context, data_dict=None):
    """
    Intercepts default resource_create action and encrypts password if resource is dataproxy type
    Args:
        context: Request context.
        data_dict: Parsed request parameters.
    Returns:
        see get_action('resource_create').
    Raises:
        Exception: if ckan.dataproxy.secret configuration not set.
    """
    #If not set, default to empty string
    url_type = data_dict.get('url_type')

    if url_type == 'dataproxy':
        secret = config.get('ckan.dataproxy.secret', False)
        if not secret:
            raise Exception('ckan.dataproxy.secret must be defined to encrypt passwords')
        password = data_dict.get('db_password')
        #replace password with a _password_ placeholder
        data_dict['url'] = data_dict['url'].replace(password, '_password_')
        #encrypt db_password
        data_dict['db_password'] = hexlify(encrypt(secret, password))

    return orig_resource_create(context, data_dict)
