import pytest

from loadbalancer import loadbalancer
import json

@pytest.fixture
def client():
    with loadbalancer.test_client() as client:
        yield client
    

def test_host_routing_mango(client):
    result = client.get('/',headers = {'Host':'www.mango.com'})
    data = json.loads(result.data.decode())
    assert b'This is the mango application' in result.data
    assert data['server'] in ['http://localhost:8082/','http://localhost:8081/']
    assert data['custom_header'] == 'Test'
    assert data['host_header'] in ['localhost:8082', 'localhost:8081']

def test_host_routing_apple(client):
    result = client.get('/',headers = {'Host':'www.apple.com'})
    data = json.loads(result.data.decode())
    assert b'This is the apple application' in result.data
    assert data['server'] in ['http://localhost:9082/','http://localhost:9081/']
    assert not data['custom_header']
    assert data['host_header'] in ['localhost:9082', 'localhost:9081']

def test_host_routing_orange(client):
    result = client.get('/',headers={'Host': 'www.orange.com'})
    assert b'No backend servers available.' in result.data

def test_host_routing_not_found(client):
    result = client.get('/',headers = {'Host':'www.notmango.com'})
    assert b'Not Found' in result.data
    assert 404 == result.status_code

def test_path_routing_mango(client):
    result = client.get('/mango')
    data = json.loads(result.data.decode())
    assert b'This is the mango application' in result.data
    assert data['server'] in ['http://localhost:8082/', 'http://localhost:8081/']
    assert not data['custom_header']
    assert data['host_header'] in ['localhost:8082', 'localhost:8081']

def test_path_routing_apple(client):
    result = client.get('/apple')
    data = json.loads(result.data.decode())
    assert b'This is the apple application' in result.data
    assert data['server'] in ['http://localhost:9082/','http://localhost:9081/']
    assert not data['custom_header']
    assert data['host_header'] in ['localhost:9082', 'localhost:9081']

def test_path_routing_orange(client):
    result = client.get('/orange')
    assert b'No backend servers available.' in result.data


def test_path_routing_not_fount(client):
    result = client.get('/notapple')
    assert b'Not Found' in result.data
    assert 404==result.status_code
