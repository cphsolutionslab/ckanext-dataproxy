import paste.fixture
import pylons.test
import pylons.config as config
import sqlalchemy
import sqlalchemy.orm as orm

import ckan.model as model
import ckan.plugins as p
import ckan.lib.create_test_data as ctd
from ckanext.datastore.tests.helpers import rebuild_all_dbs, set_url_type

import ckan.tests as tests


class TestDataproxyActions(object):
    
    @classmethod
    def setup_class(cls):
        '''Nose runs this method once to setup our test class.'''
        cls.app = paste.fixture.TestApp(pylons.test.pylonsapp)
    
    # TODO: implement tests  
    def test_this(self):
        print('this is test')