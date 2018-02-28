#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from github import Github


class GithubClient(object):

    def __init__(self, repo=None, token=None):
        if token is None:
            token = os.getenv('GITHUB_TOKEN')
        self.token = token
        self._repo = repo
        self.gh_client = Github(token)

    def _get_gh_repo(self, repo=None):
        if repo is None:
            repo = self._repo
        return self.gh_client.get_user().get_repo(repo)

    def get_labels(self, repo=None):
        gh_repo = self._get_gh_repo(repo)
        return gh_repo.get_labels()
    
    def create_label(self, label, repo=None, color='e3e3e3'):
        gh_repo = self._get_gh_repo(repo)
        gh_repo.create_label(label, color)
    
    def create_issue(self, title, body, labels, repo=None):
        """return issue id"""
        gh_repo = self._get_gh_repo(repo)
        issue = gh_repo.create_issue(title, body, labels=labels)
        return issue 
        