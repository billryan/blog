#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import argparse
from datetime import datetime

import frontmatter

from migrate import migrate, YamlContent
from githubclient import GithubClient
from util import par_dir, mkdir_p
from summary import gen_summary, update_summary

BASEDIR = os.path.abspath(os.path.dirname(__file__))
# GitHub related
OWNER = 'billryan'
REPO = 'blog'
BRANCH = 'master'
COMMENT_PREFIX = 'comment'
COMMENT_BODY = '评论专用 issue'


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
    parser.add_argument('--setup-comment', dest='setup_comment',
                        help='setup comment for blog')
    args = parser.parse_args()
    print('Called with arguments: {}'.format(args))

    ROOTDIR = par_dir(BASEDIR)
    POSTSDIR = os.path.join(ROOTDIR, 'posts')
    if args.migrate:
        migrate(args.migrate, POSTSDIR)

    if args.new:
        title = args.new
        created = curr_time()
        pardir = created[:7]  # 取年月 2018-02 为父文件夹
        metadata = {'created': created, 'title': title}
        if args.setup_comment:
            label_ = COMMENT_PREFIX + '_' + created
            gh_client = GithubClient(REPO)
            gh_client.create_label(label_)
            source_md = '[{title}](../blob/{branch}/posts/{pardir}/{created}.md)'.format(
                title=title, branch=BRANCH, pardir=pardir, created=created
            )
            body = source_md + ' ' + COMMENT_BODY
            labels = [COMMENT_PREFIX, label_]
            issue_title = '[{}] {}'.format(COMMENT_PREFIX, title)
            issue = gh_client.create_issue(issue_title, body, labels)
            print('created issue with title: {}, id: {}'.format(issue.title, issue.number))
            metadata = {'created': created, 'title': title, 'issue_id': issue.number}
        content = '# ' + title
        yaml_content = YamlContent(metadata, content)
        post_dir = os.path.join(POSTSDIR, pardir)
        post_fn = os.path.join(post_dir, created + '.md')
        mkdir_p(post_dir)
        post_md = frontmatter.dumps(yaml_content, allow_unicode=True)
        with open(post_fn, 'w', encoding='utf-8') as f:
            print('create post file {}...'.format(post_fn))
            f.write(post_md)
        # update summary
        update_summary(ROOTDIR)

    if args.fix_summary:
        update_summary(ROOTDIR)
