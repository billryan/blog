#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
from datetime import datetime

from migrate import migrate
from util import par_dir
from summary import gen_summary

BASEDIR = os.path.abspath(os.path.dirname(__file__))


def curr_time():
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Helper for GitBook blog')
    parser.add_argument('--new', type=str, dest='new',
                        help='create new post with given title.')
    parser.add_argument('--update', nargs='*', dest='update',
                        help='update post with given title in post and summary.')
    parser.add_argument('--migrate', type=str, dest='migrate',
                        help='migrate old posts(hexo)')
    parser.add_argument('--fix-summary', dest='fix_summary',
                        help='render new summary from posts.')
    args = parser.parse_args()
    print('Called with arguments: {}'.format(args))

    ROOTDIR = par_dir(BASEDIR)
    if args.migrate:
        posts_dir = os.path.join(ROOTDIR, 'posts')
        migrate(args.migrate, posts_dir)

    if args.fix_summary:
        posts_dir = os.path.join(ROOTDIR, 'posts')
        summary = gen_summary(posts_dir)
        summary_fn = os.path.join(ROOTDIR, 'SUMMARY.md')
        with open(summary_fn, 'w', encoding='utf-8') as f:
            f.write(summary)
