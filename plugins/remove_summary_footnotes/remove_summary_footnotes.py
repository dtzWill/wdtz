'''
Copyright (c) 2015 Will Dietz

remove_summary_footnotes

Plugin to strip reference footnotes from article summaries.

In summaries these footnotes don't make sense as the
reference lists (footnote targets) aren't included.
'''

import logging
from bs4 import BeautifulSoup

from pelican import signals

logger = logging.getLogger(__name__)

def remove_footnotes(content):
    '''
    Strip footnote reference links from 'content'
    '''
    if content is None:
        return None

    soup = BeautifulSoup(content)
    soup.html.unwrap()
    soup.body.unwrap()

    for ref_footnote in soup.findAll("a", class_="footnote-reference"):
        # Remove the footnote-reference link and the space preceding it
    
        # Example:
        # <a href="...">Actual link</a> <a class="footnote-reference">[1]</a>

        # Access previous element in tree.
        # This should be a 'NavigableString' with a single space.
        prev = ref_footnote.previous_sibling
        if prev.string != " ":
            raise Exception("Unexpected HTML surrounding summary footnote reference!")

        # If that went well, remove the space and the footnote tag.
        prev.replace_with("") # can't remove, replace with empty string
        ref_footnote.decompose() # remove and deconstruct

    return soup.decode()

def process(instance):
    '''
    Remove footnote references from article summary
    '''

    if hasattr(instance, '_summary'):
        instance._summary = remove_footnotes(instance._summary)


def register():
    signals.content_object_init.connect(process)
