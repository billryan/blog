#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
from collections import defaultdict

import frontmatter


def _gen_md_list_item(title, path):
    return '* [{title}]({path})'.format(title=title, path=path)


def _gen_nested_lists(parent, children):
    children_items = '\n'.join(['    ' + i for i in children])
    return parent + '\n' + children_items


def _gen_summary_posts(posts):
    posts_ = defaultdict(list)
    posts_dirname = os.path.basename(posts)
    posts_md = glob.glob(os.path.join(posts, '*/*.md'))
    for i in posts_md:
        title = frontmatter.load(i)['title']
        created = frontmatter.load(i)['created']
        dirs = i.split('/')
        postdir = dirs[-3]
        pardir = dirs[-2]
        filename = dirs[-1]
        path = '/'.join([postdir, pardir, filename])
        md_list_item = _gen_md_list_item(title, path)
        posts_[pardir].append((md_list_item, created))
    
    summary_posts = []
    for pardir in sorted(posts_.keys(), reverse=True):
        pardir_list = posts_[pardir]
        pardir_list_sorted = sorted(pardir_list, key=lambda x: x[1], reverse=True)
        children_item = [i[0] for i in pardir_list_sorted]
        pardir_md_path = '/'.join([posts_dirname, pardir, 'README.md'])
        pardir_item = _gen_md_list_item(pardir, pardir_md_path)
        summary_posts.append(_gen_nested_lists(pardir_item, children_item))
    return '\n'.join(summary_posts)


def gen_summary(posts):
    summary_posts = _gen_summary_posts(posts)
    return '\n'.join([HEADER, ABOUT, RESUME, summary_posts, TAGS, '\n'])


def update_summary(rootdir):
    postdir = os.path.join(rootdir, 'posts')
    summary = gen_summary(postdir)
    summary_fn = os.path.join(rootdir, 'SUMMARY.md')
    with open(summary_fn, 'w', encoding='utf-8') as f:
        f.write(summary)

HEADER = '# Summary\n'
ABOUT = _gen_md_list_item('关于我', 'README.md')
RESUME = _gen_md_list_item('简历', 'resume.md')
TAGS = _gen_md_list_item('Tags', 'tags.md')