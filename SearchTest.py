from flask import Flask, render_template, request, session, flash, jsonify, abort

import sqlite3 as sql
import math
import re
from markupsafe import escape
import os  # package used to generate random number
import socket
import Encryption
import pandas as pd
import hmac, hashlib


key = b'\x89\xcc\x01y\xfd\xbd\xcd=Gv\x99m\xa5\x9f?f\x02\x86\xc9#\xea\xf7\xc3e\xd6\xa0\t\x06D\xad<\x84'
iv = b'w\xdb^K%\\\xf5,`\xc7\xbb\xabs\x1f\x06\x16'
cipher = Encryption.AESCipher(key,iv)

def create_app() -> Flask:
   app = Flask(__name__)
   ...
   return app
# initialization of flask object
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/results', methods=['POST'])
def results():
    if request.method == 'POST':
        srch = request.form.get('libsearch')
        cat = request.form.get('category')

        with sql.connect("Library.db") as con:
            con.row_factory = sql.Row
            cur = con.cursor()

            if cat == 'book':
                sql_query = '''SELECT b.bookName, b.author, b.description, b.genre, l.libraryName, b.dewey \
                FROM Books b JOIN Libraries l ON b.libraryID = l.libraryID \
                WHERE b.bookName LIKE ?;'''
                cur.fetchall()
                cur.execute(sql_query, ('%'+srch+'%',))
            elif cat == 'author':
                sql_query = '''SELECT b.bookName, b.author, b.description, b.genre, l.libraryName, b.dewey \
                FROM Books b JOIN Libraries l ON b.libraryID = l.libraryID \
                WHERE b.author LIKE ?;'''
                cur.fetchall()
                cur.execute(sql_query, ('%'+srch+'%',))
            elif cat == 'genre':
                sql_query = '''SELECT b.bookName, b.author, b.description, b.genre, l.libraryName, b.dewey \
                FROM Books b JOIN Libraries l ON b.libraryID = l.libraryID \
                WHERE b.genre LIKE ?;'''
                cur.fetchall()
                cur.execute(sql_query, ('%'+srch+'%',))
            elif cat == 'library':
                sql_query = '''SELECT b.bookName, b.author, b.description, b.genre, l.libraryName, b.dewey \
                FROM Books b JOIN Libraries l ON b.libraryID = l.libraryID \
                WHERE l.libraryName LIKE ?;'''
                cur.fetchall()
                cur.execute(sql_query, ('%'+srch+'%',))
            df = pd.DataFrame(cur.fetchall(), columns=['b.bookName', 'b.author', 'b.description', 'b.genre', 'l.libraryName', 'b.dewey'])
            return render_template('results.html', rows = df)
    return render_template('search.html')

if __name__ == '__main__':
    app.secret_key = os.urandom(12)  # generate random number
    # need secret key to generate session variable
    app.run(debug=True)
