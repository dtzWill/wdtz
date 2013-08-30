'''
Copyright (c) 2013 Will Dietz

wrap_figures

Plugin to wrap figure div's to facilitate
centering and use of display:inline-block.

'''

import logging
from lxml import html
from lxml.html import builder as E
from lxml.html.clean import clean_html
from copy import deepcopy

from pelican import signals

logger = logging.getLogger(__name__)


def add_figure_wrappers(content):
    if content is None:
        return None

    tree = html.fromstring(content)
    tree = clean_html(tree)
    for figure in tree.find_class("figure"):
        wrapped = E.DIV(E.CLASS("figure-wrapper"),
                        deepcopy(figure))
        tree.replace(figure, wrapped)
    res = html.tostring(tree).decode("utf-8")

    # Blargh.  Rip out the outter div lxml adds to the html fragment.
    if res.startswith("<div>") and res.endswith("</div>"):
        res = res[5:-5]
    return res


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
