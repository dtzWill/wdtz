'''
Copyright (c) 2015 Will Dietz

nbsp_footnotes

Plugin to replace space between word and footnote with a
non-breaking space to prevent things like this
[1].

[1] Isn't this annoying?
'''

import logging
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def nbsp_footnotes(content):
    '''
    Replace space between link and footnote with nbsp.
    '''
    if content is None:
        return None

    soup = BeautifulSoup(content, "lxml")
    soup.html.unwrap()
    soup.body.unwrap()

    for ref_footnote in soup.findAll("a", class_="footnote-reference"):
        # Example:
        # <a href="...">Actual link</a> <a class="footnote-reference">[1]</a>

        # Access previous element in tree.
        # This should be a 'NavigableString' with a single space.
        prev = ref_footnote.previous_sibling
        if prev.string != " ":
            raise Exception(
                "Unexpected HTML surrounding summary footnote reference!")

        prev.replace_with(u'\xa0')  # U+00A0 = nbsp

    return soup.decode()


def process(instance):
    '''
    Make space between link and footnote non-breaking.
    '''

    if hasattr(instance, '_content'):
        instance._content = nbsp_footnotes(instance._content)
