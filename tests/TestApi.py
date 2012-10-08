import requests

def test_serverup():
    r = requests.get('http://localhost:8000')
    
    assert r.status_code == 200

def test_responseback():
    r = requests.get('http://localhost:8000')
    assert r.text == u'Hello, world'

def test_existing_data():
    r = requests.get('http://localhost:8000/v1/homedepot/deals?status=active')
    assert r.status_code == 200
    r = requests.get('http://localhost:8000/v1/lowes/deals?status=active')
    assert r.status_code == 200

def test_nonexistant_data():
    r = requests.get('http://localhost:8000/v1/nonedepot/deals?status=inactive')
    assert r.status_code == 404

def test_improper_query():
   r = requests.get('http://localhost:8000/v1/homedepot/deals?blastus=djantive111')
   assert r.status_code == 400

def test_elasticsearch_isup():
   r = requests.get('http://localhost:9200/_cluster/nodes/_local')
   assert r.status_code == 200
