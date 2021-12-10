# -*- coding: utf-8 -*-

"""An Albert extension to decode a JWT and get the fields that you want."""

from albert import info, Item, ClipAction
import jwt

__title__ = "Decode JWT"
__version__ = "0.0.1"
__triggers__ = "jwt"
__authors__ = "Jan Eisenmenger"

def get_item_for_field(field, decoded_token):
    if (field not in decoded_token):
        return Item(id = 'decode-jwt-{}'.format(field),
        text = field, 
        subtext = str('field "{}" does not exist on the jwt'.format(field)),
        actions = [])  

    
    return Item(
        id = 'decode-jwt-{}'.format(field),
        text = field, 
        subtext = str(decoded_token[field]),
        actions = [
            ClipAction(
                text=field,
                clipboardText=str(decoded_token[field])
                )]    
    )

def handleQuery(query):
    if not query.isTriggered:
        return
        
    query_tokens = list(filter(lambda t: t != '' , query.string.split(' '))) 
    if (len(query_tokens) == 0):
        return [Item(
            id = 'decode-jwt-hint',
            text = 'jwt <token>', 
            subtext = 'paste your token to decode it',
            actions = []
        )]
        
    decoded_token = {}
        
    try :
        decoded_token = jwt.decode(
            query_tokens[0],
            options={"verify_signature": False, 'verify_aud': False})
    except Exception as e: 
        return [Item(
              id = 'decode-jwt-issue',
            text = 'Could not decode the token', 
            subtext = str(e),
            actions = [] )]
        
    fields_of_interest = ['sub', 'scope', 'iss']
    
    if len(query_tokens) > 1:
        fields_of_interest.extend([query_tokens[1]])
        
    info(fields_of_interest)
     
    items = list(map(lambda f: get_item_for_field(f, decoded_token), fields_of_interest))
    items.extend([Item(
        id = 'decode-jwt-obj',
        text = 'Decoded token', 
        subtext = str(decoded_token),
        actions = [
            ClipAction(
                text='Decoded token',
                clipboardText=str(decoded_token)
                )]    
    )])        
    
    return items   
    