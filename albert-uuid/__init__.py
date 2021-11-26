# -*- coding: utf-8 -*-

"""An Albert extension that creates a uuidv4 and saves it to the clipboard"""

from albert import *
import uuid

__title__ = "UUID creator"
__version__ = "0.0.1"
__triggers__ = "uuid"
__authors__ = "Jan Eisenmenger"


def handleQuery(query):
    if not query.isTriggered:
        return
    
    new_uuid = uuid.uuid4()
       
    return [Item(id = 'uuidv4-to-clipboard',
                text = 'UUID v4', 
                subtext = str(new_uuid), 
                actions = [
                    ClipAction(
                        text='UUIDv4',
                        clipboardText=str(new_uuid)
                        )
                    ]
    )]
