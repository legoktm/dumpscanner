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


def function(**kw):
    site = pywikibot.site.APISite.fromDBName(kw['dbname'])
    languages = site.family.obsolete + site.family.langs.keys()
    for lang, title in interwikiR.findall(kw['text']):
        lang = lang.lower()
        if lang in languages:
            kw['logger'](kw['dbname'] + ': ' + kw['page'].title, lf=logfile)

if __name__ == '__main__':
    wp = scanner.get_dblist('wikipedia')
    voy = scanner.get_dblist('wikivoyage')
    scanner.run(wp+voy, function)
