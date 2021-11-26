# -*- coding: utf-8 -*-

"""An Albert extension that creates a uuidv4 and saves it to the clipboard"""

from albert import Item, FuncAction, info
import psutil
from collections import namedtuple
from fuzzywuzzy import process

__title__ = "kill-port"
__version__ = "0.0.1"
__triggers__ = "kill-port "
__authors__ = "Jan Eisenmenger"


def get_albert_item_for_port_pid_tuple(port_pid_tuple):
    info(port_pid_tuple)
    process = psutil.Process(port_pid_tuple.pid)
    
    return Item(id = 'kill-port-item-{}'.format(process.name()),
                 text = '{}:\t{}'.format(port_pid_tuple.port, process.name()), 
                 subtext = process.exe(),
                 actions=[
                    FuncAction(text= 'kill the process', callable=lambda:process.kill())
                 ])

PortPidTuple = namedtuple('PortPidTuple', 'port pid')

def get_port_pid_tuples():
    port_pid_tuples = []
    
    for local_connection in psutil.net_connections():
        if (local_connection.pid is None or local_connection.status == psutil.CONN_NONE):
            continue
                
        port_pid_tuples.append(PortPidTuple(local_connection.laddr.port, local_connection.pid))
    return port_pid_tuples
    

def funcForProcessor(t):
    info(t)
    return t.port
    
def handleQuery(query):
    if not query.isTriggered:
        return
    
    query_tokens = query.string.split(' ')
    
    if (len(query_tokens[0].strip()) == 0):
        return [Item(id = 'kill-port-error',
                 text = 'kill-port [port-number]', 
                 subtext = 'will kill it for good.')] 
    
    port_number = 0
    try: 
        port_number = int(query_tokens[0])
        if (port_number < 1 or port_number > 65535):
            raise ValueError('Invalid port number')
    except:    
       return [Item(id = 'kill-port-error',
                 text = 'Error', 
                 subtext = 'Your argument "{}" is not a valid port number.'.format(query_tokens[0]), 
     )]
    
    
    port_pid_tuples = get_port_pid_tuples()

    info (port_pid_tuples[0])
    [list_of_ports, list_of_pids] = zip(*port_pid_tuples)
    
    relevant_port_result =  process.extract(str(port_number), list_of_ports, limit=5)
    relevant_port_result = filter(lambda rpr: rpr[1] > 75, relevant_port_result)
    relevant_ports = list(map(lambda rpr: rpr[0], relevant_port_result))
    
    info(relevant_ports)
    
    if (len(relevant_ports) == 0):
        return [Item(id = 'kill-port-no-process',
                 text = 'Could not find a process running on port {}.'.format(port_number), 
                 subtext = ' Try a different one.', 
     )]
        
    relevant_port_pid_tuples = filter(lambda t: t.port in relevant_ports, port_pid_tuples)
        
    items = list(map(get_albert_item_for_port_pid_tuple, relevant_port_pid_tuples))

    return items