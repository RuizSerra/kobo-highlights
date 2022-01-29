#!/usr/bin/env python

"""
To show Kobo highlights and annotations in the browser.

Author: Jaime Ruiz Serra
Date:   Feb 2021

Helpful: https://inloop.github.io/sqlite-viewer/
"""

from flask import Flask, render_template
from markupsafe import escape
import urllib.parse

import kobuddy

DB_FILENAME = '/Users/jaime/Documents/kobo/kobo-backup/KoboReader-20220129-copy.sqlite'

app = Flask(__name__)


# Data retrieval ---------------------------------------------------------------

def get_highlights(db_filename):
    with kobuddy.set_databases(db_filename):
        highlights = kobuddy.get_highlights()
    return highlights

def get_books(db_filename):
    with kobuddy.set_databases(db_filename):
        books = kobuddy.get_books()
    return books


# Front end --------------------------------------------------------------------

@app.route('/book/<book_query>')
def show_book_highlights(book_query):

    highlights = get_highlights(DB_FILENAME)
    book_query = escape(book_query)

    matching_books = set([h.book for h in highlights
                          if book_query.lower() in str(h.book).lower()])

    book_highlights = {b:[] for b in matching_books}
    for h in highlights:
        if h.book in book_highlights:
            book_highlights[h.book].append(h)

    return render_template('book.html',
                           book_query=book_query,
                           book_highlights=book_highlights)


@app.route('/')
def index():
    books = get_books(DB_FILENAME)
    highlights = get_highlights(DB_FILENAME)

    book_counts = {b: 0 for b in books}
    for h in highlights:
        book_counts[h.book] += 1

    return render_template('index.html',
                           book_counts=book_counts)
