'''
Copyright (c) 2015 Will Dietz

replace_tt

Plugin to find instances of 'tt' tag and replace with 'code'.
'tt' is non-standard and deprecated in HTML5.

Presently 'tt' tags are generated for inline code, which will now be 'code' and need styling.
'''

import logging
from bs4 import BeautifulSoup

from pelican import signals

logger = logging.getLogger(__name__)

def replace_tt(content):
    '''
    Replace 'tt' tags with 'code'.
    '''
    if content is None:
        return None

    soup = BeautifulSoup(content)
    soup.html.unwrap()
    soup.body.unwrap()

    for div in soup.findAll('tt'):
        div.name = 'code'

    return soup.decode()

def process(instance):
    '''
    Replace tt with code in post 'instance'
    '''

    if hasattr(instance, '_content'):
        instance._content = replace_tt(instance._content)
    if hasattr(instance, '_summary'):
        instance._summary = replace_tt(instance._summary)
