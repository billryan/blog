#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
from datetime import datetime

def migrate(posts):
    _posts = glob.glob(os.path.join(posts, '*.md'))
    for p in _posts:
        with open(p) as f:
            contents = f.read()
        suffix_len = -1 * len('2010-12/2010-12-13_23-50-20.md')
        url = 'url:  "/posts/{}/"'.format(p[suffix_len:-3])
        c = contents.replace('\n---\n', '\n' + url + '\n---\n')
        with open(p, 'w') as f:
            f.write(c)

if __name__ == '__main__':
    migrate('content/post/*/')
