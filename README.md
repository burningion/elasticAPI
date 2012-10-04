Tornado and Elasticsearch Example Webapp
========================================

This is an example application to demonstrate building a basic API with Tornado and ElasticSearch.

It can be deployed with the following command:

>> $ gunicorn -k egg:gunicorn#tornado webapp:app

Once deployed, you can run the nosetests, to verify the API works. I should make this run on a different port when testing, that would be smart.

# DONE

Implement RESTful calls for the following URLS:

http://localhost/<CLIENTNAME>/deals?status=active

http://localhost/<CLIENTNAME>/deals?status=inactive

Although that's ugly, we always change things in the future, so let's add a version system to the requirements.

Changed RESTful calls for the URLS:

http://localhost/v1/<CLIENTNAME>/deals?status=active

http://localhost/v1/<CLIENTNAME>/deals?status=inactive

Test by running nosetests in the root directory.

## Install test data with ipython:

`
$ ipython

import schema
schema.create_and_insert()
`

## Run the gunicorn server:
`
$ gunicorn -k egg:gunicorn#tornado webapp:app 
`