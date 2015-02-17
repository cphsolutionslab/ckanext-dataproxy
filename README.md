ckanext-dataproxy
=========
ckanext-dataproxy is [CKAN](https://github.com/ckan/ckan) extension that enables previewing data from remote databases via SQLAlchemy. The extension is compatible with datastore by masking the dataproxy resource as a datastore resource so it could be requested via api/3/action/datastore_search or previewed in-browser with recline-preview.

Usage
-------
*Using this module assumes that CKAN server can access the database which is being proxied via resource.*

Create a dataset and navigate to resource adding form:
![create-resource](http://i.imgur.com/B7jAl7T.png)

Upon clicking on the DataProxy button, following fields appear:
![dataproxy-fields](http://i.imgur.com/iQexXDM.png)

 - The interface assists by providing default ports for various database types
 - Connection string (URL field) is automatically generated based on entered values
 - Connection string can be modified to pass additional parameters if necessary
 - Password will be encrypted with AES256 block cipher and replaced with \_password\_ placeholder

Upon navigating to the resource, recline will automatically render preview:
![recline-preview](http://i.imgur.com/OCA4tMf.png)
The resource is also accessible at api/3/action/datastore_search regardless if datastore extension itself is set up or not. The API response format is compatible with datastore resources*

Installing
-------
1) Clone this repo  
`cd /usr/lib/ckan/default/src`  
`git clone TODO!`  
`cd ckanext-dataproxy`  
 2) Install requirements (It is not required to install drivers for databases you don't plan to proxy, see the file)  
` pip install -r requirements.txt`  
*Additional packages may be required to compile the drivers, for ubuntu:*  
`sudo apt-get install build-essentials libmysqlclient-dev freetds-dev`  
3) Install the plugin  
`python setup.py develop`  
4) Edit ckan settings file e.g /etc/ckan/default/production.ini  
`#Password for AES256 key generation (Any string will do e.g)`  
` ckan.dataproxy.secret = c10cef60c700034657feb6e12304a`  
5) Enable the plugin, append 'dataproxy' to plugins:  
`ckan.plugins = stats text_preview ... dataproxy`  

Tests
-------
TODO: No unit-tests currently

Known bugs
-------
1. if resource is file upload, then 'dataproxy' button will appear next to 'remove' button
2. can not change resource type to 'dataproxy' from existing resource, however existing 'dataproxy' resource can be changed to other type
3. download entire resource as csv not implemented
