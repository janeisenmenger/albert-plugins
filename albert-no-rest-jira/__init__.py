# -*- coding: utf-8 -*-

"""An Albert extension that allows you to talk to jira."""

from albert import *
import json
import os.path
from urllib.parse import urlparse


__title__ = "Jira no-REST"
__version__ = "0.0.1"
__triggers__ = "jira "
__authors__ = "Jan Eisenmenger"

commands = ['change-server', 'view', 'show-config']

def get_config_path(): 
    return configLocation() + '/jira-no-rest_config.json'

def get_config():
    try:
        with open(get_config_path(), 'r') as config_file:
            return json.load(config_file)
    except Exception as e:
        info(str(e))
        return {}

def write_config(config):
    with open(get_config_path(), 'w+') as config_file:
            json.dump(config, config_file)

def change_server_item(new_server_url, config):   
    def handle_enter_server_url(): 
        config['server_url'] = new_server_url.rstrip('/')
        write_config(config)
    
    return [Item(id = 'jira-no-rest-enter-server-url',
                text = 'Enter the JIRA server url', 
                subtext = 'whatever you type after "jira" will be used.', 
                actions = [
                    FuncAction(text= 'enter new server url', callable=handle_enter_server_url)
                ]
        )] 

def view_issue(issue_key, config):
    server_url = config.get('server_url')
    if (server_url == None):
        return
    return Item(
            id = 'jira-view-issue',
            text = 'view issue', 
            subtext = 'will view the issue ' + issue_key,
            actions = [
                UrlAction(text="view issue", url = server_url + '/browse/' + issue_key)
            ]
        )    

def check_valid_config(config, query):
    if config.get('server_url') == None:
        return change_server_item(query.string, config)
        
    return

def handleQuery(query):
    if not query.isTriggered:
        return
    
    config = get_config()
    valid_config_result = check_valid_config(config, query)
    
    if (valid_config_result != None):
        return valid_config_result
        
    query_tokens = query.string.split(' ')
    if (query_tokens[0] not in commands):
        return [
        Item(
            id = 'jira-change-server-url',
            text = 'change-server', 
            subtext = 'use keyword "change-server" to change the server url',
            completion=__triggers__ + 'change-server ',
            actions = []
        ),
        Item(
            id = 'jira-view-issue',
            text = 'view', 
            subtext = 'use keyword "view" to view an issue',
            completion=__triggers__ + 'view ',
            actions = []
        )
        ]
        
    if (query_tokens[0] == 'change-server'):
        return change_server_item(query_tokens[1], config)
    if (query_tokens[0] == 'view'):
        return view_issue(query_tokens[1], config)


        
    return [Item(
            id = 'jira-no-rest-enter-server-url',
            text = 'Look at my config my config is amazing!', 
            subtext = str(config), 
            actions = []
        )] 