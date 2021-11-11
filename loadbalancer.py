from flask import Flask,request
import requests
import random
import yaml

from utils import (
    get_healthy_server, 
    healthcheck,
    process_rewrite_rules,
    process_rules, 
    transform_backends_from_config,
    load_configuration
)

loadbalancer = Flask(__name__)

# MANGO_BACKENDS = ['localhost:8081','localhost:8082']
# APPLE_BACKENDS = ['localhost:9081','localhost:9082']

config = load_configuration('loadbalancer.yaml')
register = transform_backends_from_config(config)

@loadbalancer.route('/')
@loadbalancer.route('/<path>')
def router(path='/'):
    updated_register = healthcheck(register)
    # print(updated_register)
    host_header = request.headers['Host']
    # print(host_header)
    for entry in config['hosts']:
        if host_header == entry['host']:
            healthy_server = get_healthy_server(entry['host'],updated_register)
            if not healthy_server:
                return 'No backend servers available.', 503
            headers = process_rules(config,host_header, {k:v for k,v in request.headers.items()},'header')
            params = process_rules(config,host_header,{k:v for k,v in request.args.items()},'param')
            rewrite_path = ''
            if path=='v1':
                rewrite_path = process_rewrite_rules(config,host_header,path)
            resp = requests.get(f'http://{healthy_server.endpoint}/{rewrite_path}', headers=headers,params=params)
            return resp.content, resp.status_code
    
    for entry in config['paths']:
        if '/' + path == entry['path']:
            healthy_server = get_healthy_server(entry['path'],register)
            if not healthy_server:
                return 'No backend servers available.',503
            resp = requests.get(f'http://{healthy_server.endpoint}')
            return resp.content,resp.status_code
    # if host_header == 'www.mango.com':
    #     resp = requests.get(f'http://{random.choice(MANGO_BACKENDS)}')
    #     return resp.content,resp.status_code
    # elif host_header=='www.apple.com':
    #     resp = requests.get(f'http://{random.choice(APPLE_BACKENDS)}')
    #     return resp.content,resp.status_code
    # else:
    #     return 'Not Found',404
    return 'Not Found',404

# @loadbalancer.route('/mango')
# def mango_path():
#     resp = requests.get(f'http://{random.choice(MANGO_BACKENDS)}')
#     return resp.content, resp.status_code

# @loadbalancer.route('/apple')
# def apple_path():
#     resp = requests.get(f'http://{random.choice(APPLE_BACKENDS)}')
#     return resp.content, resp.status_code

# @loadbalancer.route('/<path>')
# def path_router(path):
#     for entry in config['paths']:
#         if '/'+path == entry['path']:
#             resp = requests.get(f'http://{random.choice(entry["servers"])}')
#             return resp.content,resp.status_code
#     return 'Not Found',404

if __name__=='__main__':
    loadbalancer.run(host='0.0.0.0')