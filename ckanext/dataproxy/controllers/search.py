import urllib
import json
import decimal
import datetime
import pylons
from ckan.controllers.api import ApiController
import ckan.logic as logic
from sqlalchemy import *
from ckan.model import Resource
from collections import OrderedDict
from simplecrypt import decrypt
from binascii import unhexlify

def alchemyencoder(obj):
    """JSON encoder function for SQLAlchemy special classes."""
    #By default python can't even serialize it's own datetime & decimal classes
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    elif isinstance(obj, decimal.Decimal):
        return float(obj)

class SearchController(ApiController):
    """Searchcontroller overrides datastore search_action API endpoint if it exists
    or creates one if datastore is disabled so that dataproxy can be used independantly"""

    def search_action(self):
        """Routes dataproxy type resources to dataproxy_search method, else performs 'datastore_search' action"""
        #TODO: No access control checks for dataproxy resources!
        request_data = self._get_request_data(try_url_params=True)
        resource = Resource.get(request_data['resource_id'])
        if resource is not None and resource.url_type == 'dataproxy':
            pylons.response.headers['Content-Type'] = 'application/json;charset=utf-8'
            return self.dataproxy_search(request_data, resource)

        #Default action otherwise
        return self.action('datastore_search', ver=3)

    def dataproxy_search(self, request_data, resource):
        """Performs actual query on remote database via SqlAlchemy
        Args:
            request_data: Dictionary of parsed request parameters.
            resource: Resource object that is being searched.
        Returns:
            Datastore search compatible JSON object with search results.
        Raises:
            Exception: if ckan.dataproxy.secret configuration not set.
        """
        secret = pylons.config.get('ckan.dataproxy.secret', False)
        if not secret:
            raise Exception('ckan.dataproxy.secret must be defined to encrypt/decrypt passwords')

        connstr = resource.url
        password = resource.extras['db_password']

        password = decrypt(secret, unhexlify(password))

        connstr = connstr.replace('_password_', password)
        table_name = resource.extras['table']

        meta = MetaData()
        #TODO: remove these
        #engine = create_engine('postgresql://ckan_default:ckan_default@localhost/datastore_default')
        #engine = create_engine('mssql+pymssql://user:pass@10.0.1.6/Northwind')
        engine = create_engine(connstr)
        table = Table(table_name, meta, autoload=True, autoload_with=engine)
        conn = engine.connect()
        select_query = select([table])
        fields = self._get_fields(table)

        limit = request_data.get('limit', None)
        offset = request_data.get('offset', None)
        filters = request_data.get('filters', None)
        sort = request_data.get('sort', None)
        q = request_data.get('q', None) #Not supported

        if limit is not None:
            select_query = select_query.limit(limit)
        if offset is not None:
            select_query = select_query.offset(offset)
        if sort is not None:
            #check if column exists
            sort_column, sort_order = sort.split(' ')
            if sort_order == 'asc':
                select_query = select_query.order_by(getattr(table.c, sort_column))
            if sort_order == 'desc':
                select_query = select_query.order_by(desc(getattr(table.c, sort_column)))
            #else unknown order
        if filters is not None:
            for field, value in filters.iteritems():
                #check if fields exists
                select_query = select_query.where(getattr(table.c, field) == value)
                
        result = conn.execute(select_query)
        r = list()
        count = 0
        for row in result:
            count += 1
            d = OrderedDict()
            for field in fields:
                d[field['id']] = row[field['id']]
            r.append(d)
        
        retval = OrderedDict()
        retval['help'] = self._help_message()
        retval['success'] = True
        retval['result'] = OrderedDict()
        retval['result']['resource_id'] = request_data['resource_id']
        retval['result']['fields'] = fields
        retval['result']['records'] = r
        if filters is not None:
            retval['result']['filters'] = filters
        if limit is not None:
            retval['result']['limit'] = limit
        if offset is not None:
            retval['result']['offset'] = offset
        if sort is not None:
            retval['result']['sort'] = sort
        if q is not None:
            retval['result']['q'] = ''
        if count:
            retval['result']['total'] = count
        retval['result']['_links'] = self._insert_links(limit, offset)

        return json.dumps(retval, default=alchemyencoder)

    def _get_fields(self, table):
        """
        Extracts field names and types from SqlAlchemy table object
        Args:
            table: SqlAlchemy Table object.
        Returns:
            list of dict objects containing 'id' and 'type' keys
            NB: The returned column types are not compatible with column types returned by datastore.
            This is due to fact that other DB types have different column types/names/sizes. The types
            could be translated to postgresql equivalent however.
        """
        fields = list()
        for column in table.columns:
            fields.append({'id': column.name, 'type': str(column.type)})
        return fields

    def _insert_links(self, limit, offset):
        """Copied from ckanext.datastore.db _insert_links() method to decouple from datastore extension"""
        if limit is None:
            limit = 0
        if offset is None:
            offset = 0

        import ckan.plugins.toolkit as toolkit
        import urllib
        import urllib2
        import urlparse
        '''Adds link to the next/prev part (same limit, offset=offset+limit)
        and the resource page.'''
        links = {}
    
        # get the url from the request
        try:
            urlstring = toolkit.request.environ['CKAN_CURRENT_URL']
        except TypeError:
            return  # no links required for local actions
    
        # change the offset in the url
        parsed = list(urlparse.urlparse(urlstring))
        query = urllib2.unquote(parsed[4])
    
        arguments = dict(urlparse.parse_qsl(query))
        arguments_start = dict(arguments)
        arguments_prev = dict(arguments)
        arguments_next = dict(arguments)
        if 'offset' in arguments_start:
            arguments_start.pop('offset')
        arguments_next['offset'] = int(offset) + int(limit)
        arguments_prev['offset'] = int(offset) - int(limit)
    
        parsed_start = parsed[:]
        parsed_prev = parsed[:]
        parsed_next = parsed[:]
        parsed_start[4] = urllib.urlencode(arguments_start)
        parsed_next[4] = urllib.urlencode(arguments_next)
        parsed_prev[4] = urllib.urlencode(arguments_prev)
    
        # add the links to the data dict
        links['start'] = urlparse.urlunparse(parsed_start)
        links['next'] = urlparse.urlunparse(parsed_next)
        if int(offset) - int(limit) > 0:
            links['prev'] = urlparse.urlunparse(parsed_prev)
        return links

    def _help_message(self):
        return """Search a DataProxy resource.
        The dataproxy_search allows you to query data in a remote database.
        :param resource_id: id or alias of the resource to be searched against
        :type resource_id: string
        :param filters: matching conditions to select, e.g {"key1": "a", "key2": "b"} (optional)
        :type filters: dictionary
        :param limit: maximum number of rows to return (optional, default: 100)
        :type limit: int
        :param offset: offset this number of rows (optional)
        :type offset: int
        :param fields: fields to return (optional, default: all fields in original order)
        :type fields: list or comma separated string
        :param sort: comma separated field names with ordering
                     e.g.: "fieldname1, fieldname2 desc"
        :type sort: string

        **Results:**

        The result of this action is a dictionary with the following keys:

        :rtype: A dictionary with the following keys
        :param fields: fields/columns and their extra metadata
        :type fields: list of dictionaries
        :param offset: query offset value
        :type offset: int
        :param limit: query limit value
        :type limit: int
        :param filters: query filters
        :type filters: list of dictionaries
        :param total: number of total matching records
        :type total: int
        :param records: list of matching results
        :type records: list of dictionaries
        """
