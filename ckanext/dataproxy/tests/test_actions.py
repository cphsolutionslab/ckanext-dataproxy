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

#import ckanext.realtime as rt


class TestRealtimeActions(object):
    ''' Tests for actions ckanext.realtime.logic.action module
    '''
    sysadmin_user = None
    normal_user = None
    
    @classmethod
    def setup_class(cls):
        '''Nose runs this method once to setup our test class.'''        
        # Make the Paste TestApp that we'll use to simulate HTTP requests to
        # CKAN.
        cls.app = paste.fixture.TestApp(pylons.test.pylonsapp)

        
        #engine = sqlalchemy.create_engine(config['ckan.datastore.write_url'])
        #cls.Session = orm.scoped_session(orm.sessionmaker(bind=engine))
        
        #rebuild_all_dbs(cls.Session)
        #p.load('datastore')
        
        #ctd.CreateTestData.create()
        
        #cls.sysadmin_user = model.User.get('testsysadmin')
        #cls.normal_user = model.User.get('annafan')
        
        # make test resource writable through action api
        #set_url_type(
            #model.Package.get('annakarenina').resources, cls.sysadmin_user)
        
        #cls._create_test_datastore()

    
    @classmethod
    def _create_test_datastore(cls):
        #print('create test datastore')
        #resource = model.Package.get('annakarenina').resources[0]
        #tests.call_action_api(cls.app, 'datastore_create',
                              #resource_id=resource.id,
                              #apikey=cls.sysadmin_user.apikey)

    @classmethod
    def teardown_class(cls):
        '''Nose runs this method once after all the test methods in our class
        have been run.
        '''
        #rebuild_all_dbs(cls.Session)
        
        # unload plugins
        #p.unload('datastore')
    
    # realtime_make_observable tests    
    def test_make_observable_by_admin(self):
        print('this is test')
        #self.assertEquals(2,1)
        #resource = model.Package.get('annakarenina').resources[0]
  
        #tests.call_action_api(self.app, 'datastore_make_observable',
                              #resource_id=resource.id,
                              #apikey=self.sysadmin_user.apikey)
