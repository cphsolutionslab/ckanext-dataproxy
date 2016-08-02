Tests
-------
TODO: No unit-tests currently

TODO: Implement access checks at overriden datastore_search api endpoint

TODO: Rename module to ckanext-database_proxy to avoid confusion with dataproxy module

TODO: Implement view filters for dataproxy resources (currently adding filters is disabled)

Known bugs
-------
1. if resource is file upload, then 'dataproxy' button will appear next to 'remove' button
2. can not change resource type to 'dataproxy' from existing resource, however existing 'dataproxy' resource can be changed to other type
3. download entire resource as csv not implemented
4. adding view filters has been disabled for dataproxy resources
