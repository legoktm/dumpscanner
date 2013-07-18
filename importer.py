#!/usr/bin/env python
"""
Copyright (C) 2013 Legoktm

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
IN THE SOFTWARE.
"""

import ast
import os
import oursql

#2013-07-11 09:58:37.744094: u'abwiki: 10: \u0410\u0448\u0430\u0431\u043b\u043e\u043d:See also: 1'

filename = '/data/project/addbot/iw_scanner.log'


def gen():
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip()
            yield parse_line(line)

def main():
    db = oursql.connect(raise_on_warnings=False,
                        read_default_file=os.path.expanduser("~/replica.my.cnf"),
                        host='tools-db',
                        db='p50380g40022_wikidata_p'
                        )
    cursor = db.cursor()
    cursor.executemany('INSERT INTO `iwlink` VALUES (?,?,?,?,?,?,?)', gen())


def parse_line(line):
    line = line[28:]
    line = ast.literal_eval(line)
    sp = line.split(': ')
    dbname = sp[0]
    if dbname.endswith('wiki'):
        lang = dbname.replace('wiki', '')
        site = 'wiki'
    else:
        lang = db.name.replace('wikivoyage', '')
        site = 'wikivoyage'
    namespace = int(sp[1])
    if ':' in sp[2]:
        title = sp[2].split(':', 1)[1]
    else:
        title = sp[2]
    links = int(sp[3])
    return site, lang, namespace, title, links, None, None

if __name__ == '__main__':
    main()