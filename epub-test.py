import ebooklib
from ebooklib import epub

from bs4 import BeautifulSoup

def epub2thtml(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return chapters


def chap2text(chap, blacklist=['[document]',
                               'noscript',
                               'header',
                               'html',
                               'meta',
                               'head',
                               'input',
                               'script']):
    output = ''
    soup = BeautifulSoup(chap, 'html.parser')
    text = soup.find_all(text=True)
    for t in text:
        if t.parent.name not in blacklist:
            output += '{} '.format(t)
    return output

def thtml2ttext(thtml):
    Output = []
    for html in thtml:
        text =  chap2text(html)
        Output.append(text)
    return Output


def epub2text(epub_path):
    chapters = epub2thtml(epub_path)
    ttext = thtml2ttext(chapters)
    return ttext

FILENAME = '/Users/jaime/Downloads/(Zero Books) Mark Fisher - Capitalist Realism_ Is there no alternative_-John Hunt Publishing (2009).epub'
out = epub2text(FILENAME)






##################################


FILENAME = '/Users/jaime/Downloads/Colorless Tsukuru Tazaki and His Years of Pilgrimage_ A novel (Vintage International) - Haruki Murakami.epub'
book = epub.read_epub(FILENAME)
# Get StartContainerPath from https://inloop.github.io/sqlite-viewer/
HIGHLIGHT_TEXT = 'It means leaving behind your physical body. Leaving the cage of your physical flesh, breaking free of the chains, and letting pure logic soar free. Giving a natural life to logic. That’s the core of free thought.'
start_container_path = 'text/part0010.html#point(/1/4/168/1:3)'
loc = book.get_item_with_href('text/part0010.html')


# This page https://www.mobileread.com/forums/showthread.php?t=319659
# makes sense of the point(/1/4/168/1:3) path

import xml.etree.ElementTree as ET
root = ET.fromstring(loc.content)

# The path of the elem containing the text does not match the path "point(/1/4/168/1:3)"
root[1][83]



def rec_search(xml_element, target = 'It means leaving behind', stack=[], path=[]):
    pprint.pprint(path)
    if len([c for c in xml_element]):
        stack += [c for c in xml_element]
        path.append(xml_element)
    if not stack:
        print('empty stack')
        return
    c = stack.pop()
    if c.text and target in c.text:
        print('FOUND')
        return path
    else:
        return rec_search(c, target=target, stack=stack, path=path)
