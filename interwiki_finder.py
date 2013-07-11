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

import pywikibot
import os
import re
import scanner

logfile = os.path.expanduser('~/public_html/iw_scanner.log')

interwikiR = re.compile(r'\[\[([a-zA-Z\-]+)\s?:([^\[\]\n]*)\]\]')
tags = ['comments', 'nowiki', 'pre', 'source']


class Holder:
    def __init__(self):
        self.counter = 0
        self.link_counter = 0
        self.site = None
        self.dbname = ''

    def function(self, **kw):
        if kw['dbname'] != self.dbname:
            self.dbname = kw['dbname']
            print 'Starting ' + self.dbname
            self.site = pywikibot.site.APISite.fromDBName(self.dbname)
        languages = self.site.family.obsolete.keys() + self.site.family.langs.keys()
        match = False
        c = 0
        for lang, title in interwikiR.findall(kw['page'].text):
            lang = lang.lower()
            if lang in languages:
                c += 1
                match = True
        if not match:
            return
        self.counter += 1
        self.link_counter += c
        print ' : '.join([str(self.counter), str(self.link_counter)])
        msg = ': '.join([self.dbname, str(kw['page'].ns), kw['page'].title, str(c)])
        kw['logger'](msg, lf=logfile)

if __name__ == '__main__':
    wp = scanner.get_dblist('wikipedia')
    voy = scanner.get_dblist('wikivoyage')
    wikis = wp + voy
    for db in scanner.get_dblist('closed'):
        if db in wikis:
            wikis.remove(db)
    h = Holder()
    scanner.run(wikis, h.function)
