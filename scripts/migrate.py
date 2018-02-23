#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import glob
from datetime import datetime

import frontmatter

from util import mkdir_p


class YamlContent(object):
    def __init__(self, metadata, content):
        self.metadata_ = metadata
        self.content_ = content
    
    @property
    def metadata(self):
        return self.metadata_
    
    @property
    def content(self):
        return self.content_


def migrate(posts, posts_new):
    print('path of posts_old: {}, posts_new: {}'.format(posts, posts_new))
    _posts = glob.glob(os.path.join(posts, '*.md'))
    for p in _posts:
        metadata, content = _migrate(p)
        yaml_content = YamlContent(metadata, content)
        created = metadata['created']
        pardir = created[:7]  # 取年月 2018-02 为父文件夹
        post_dir = os.path.join(posts_new, pardir)
        post_fn = os.path.join(post_dir, created + '.md')
        mkdir_p(post_dir)
        post_md = frontmatter.dumps(yaml_content, allow_unicode=True)
        with open(post_fn, 'w', encoding='utf-8') as f:
            print('write post file {}...'.format(post_fn))
            f.write(post_md)

def _migrate(post):
    print('migrate post {}'.format(post))
    # 处理首行不含 --- 的文档
    with open(post) as f:
        contents = f.read()
        if not contents.startswith('---'):
            contents = '---\n' + contents

    post_yaml = frontmatter.loads(contents)
    _date = post_yaml['date']
    if not isinstance(_date, str):
        _date = _date.strftime('%Y-%m-%d %H:%M:%S')
    try:
        _date_dt = datetime.strptime(_date, '%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        _date_dt = datetime.strptime(_date, '%Y-%m-%d %H:%M')
    except Exception as e:
        print(e)
        raise

    metadata = {}
    metadata['created'] = _date_dt.strftime('%Y-%m-%d_%H-%M-%S')

    title = post_yaml['title']
    metadata['title'] = title
    # 正文首行补充一级标题
    content = '# ' + title + '\n\n' + post_yaml.content
    return (metadata, content)
    