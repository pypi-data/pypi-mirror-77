#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Author: Jialiang Shi
from sonarqube.config import (
    API_PROJECT_LINKS_CREATE_ENDPOINT,
    API_PROJECT_LINKS_DELETE_ENDPOINT,
    API_PROJECT_LINKS_SEARCH_ENDPOINT
)


class SonarQubeProjectLinks:
    def __init__(self, sonarqube):
        self.sonarqube = sonarqube

    def create_project_link(self, projectKey, name, url):
        """
        Create a new project link.

        :param projectKey: Project key
        :param name: Link name
        :param url: Link url
        :return:
        """
        params = {
            'projectKey': projectKey,
            'name': name,
            'url': url
        }
        self.sonarqube.make_call('post', API_PROJECT_LINKS_CREATE_ENDPOINT, **params)

    def delete_project_link(self, link_id):
        """
        Delete existing project link.

        :param link_id: Link id
        :return:
        """
        params = {
            'id': link_id
        }
        self.sonarqube.make_call('post', API_PROJECT_LINKS_DELETE_ENDPOINT, **params)

    def search_project_links(self, projectKey):
        """
        List links of a project.

        :param projectKey: Project Key
        :return:
        """
        params = {
            'projectKey': projectKey
        }
        resp = self.sonarqube.make_call('get', API_PROJECT_LINKS_SEARCH_ENDPOINT, **params)
        response = resp.json()
        return response["links"]
