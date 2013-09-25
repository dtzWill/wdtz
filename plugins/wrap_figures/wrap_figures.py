'''
Copyright (c) 2013 Will Dietz

wrap_figures

Plugin to wrap figure div's to facilitate
centering and use of display:inline-block.

'''

import logging
from bs4 import BeautifulSoup

from pelican import signals

logger = logging.getLogger(__name__)


def add_figure_wrappers(content):
    if content is None:
        return None

    soup = BeautifulSoup(content)

    for div in soup.findAll('div'):
        if 'figure' in div['class']:
            wrap = soup.new_tag('div')
            wrap['class']="figure-wrapper"

            # Replace with wrapper,
            # and put figure inside (append)
            wrap.append(div.replace_with(wrap))

    return soup.decode()

def wrap_figures(instance):
    '''
    Wrap figures in another div for css goodness.
    '''

    if instance._content is not None:
        instance._content = add_figure_wrappers(instance._content)
        if hasattr(instance, '_summary'):
            instance._summary = add_figure_wrappers(instance._summary)


def register():
    signals.content_object_init.connect(wrap_figures)