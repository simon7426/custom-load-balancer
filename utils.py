import yaml
from models import Server
import random

def load_configuration(path):
    with open(path) as config_file:
        config = yaml.load(config_file,Loader=yaml.FullLoader)
    return config

def transform_backends_from_config(config):
    register = {}
    for entry in config.get('hosts', []):
        register.update({entry['host']: [Server(endpoint) for endpoint in entry['servers']]})
    for entry in config.get('paths', []):
        register.update({entry['path']: [Server(endpoint) for endpoint in entry['servers']]})
    return register

def get_healthy_server(host, register):
    try:
        return random.choice([server for server in register[host] if server.healthy])
    except IndexError:
        return None

def healthcheck(register):
    for host in register:
        for server in register[host]:
            server.healthcheck_and_update_status()
    return register

def load_configuration(path):
    with open(path) as config_file:
        config = yaml.load(config_file,Loader=yaml.FullLoader)
    return config

def process_header_rules(config, host, rules):
    for entry in config.get('hosts', []):
        if host == entry['host']:
            header_rules = entry.get('header_rules', {})
            for instruction, modify_headers in header_rules.items():
                if instruction == 'add':
                    rules.update(modify_headers)
                if instruction == 'remove':
                    for key in modify_headers.keys():
                        if key in rules:
                            rules.pop(key)
    return rules