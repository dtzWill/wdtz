'''
Copyright (c) 2015 Will Dietz

unify_footnotes

Plugin to find reference tables (generated by 'target-notes')
and unify them into a single HTML5-compliant block.
'''

import logging
from bs4 import BeautifulSoup, NavigableString

from pelican import signals

logger = logging.getLogger(__name__)

def unify_footnotes(content):
    '''
    Find footnote tables and unify them.
    '''
    if content is None:
        return None

    soup = BeautifulSoup(content)
    soup.html.unwrap()
    soup.body.unwrap()

    footnote_tables = soup.findAll('table', class_="docutils footnote")

    # If no footnotes, nothing to do here
    if len(footnote_tables) == 0:
        return content

    # Gather footnotes into single div
    footnotes_div = soup.new_tag('div')
    footnotes_div['class'] = "footnote-table"

    # Insert into document tree before first footnote
    footnote_tables[0].insert_before(footnotes_div)

    # Generate code for each footnote
    for t in footnote_tables:
        # Gather information we want from the original entry
        f_id = t['id']
        f_label = t.find('a', class_='fn-backref')
        f_link = t.find('a', class_='reference')

        # For styling purposes (eek) make each footnote its own table for now.
        table = soup.new_tag('table',id=f_id)
        table['class']='footnote'

        row = soup.new_tag('tr')

        label = soup.new_tag('td')
        label['class']='label'
        label.append(f_label)

        link = soup.new_tag('td')
        link.append(f_link)

        row.append(soup.new_string('\n\t'))
        row.append(label)
        row.append(soup.new_string('\n\t'))
        row.append(link)
        row.append(soup.new_string('\n'))

        table.append(row)

        footnotes_div.append(soup.new_string('\n'))
        footnotes_div.append(table)

        # Remove extraneous whitespace after the table
        after = t.next_sibling
        if isinstance(after, NavigableString):
            after.replace_with(after.strip())

        # Remove original tbale
        t.decompose()

    footnotes_div.append(soup.new_string('\n'))


    return soup.decode()

def process(instance):
    '''
    Replace footnote references with unified table
    '''

    if hasattr(instance, '_content'):
        instance._content = unify_footnotes(instance._content)


def register():
    signals.content_object_init.connect(process)
