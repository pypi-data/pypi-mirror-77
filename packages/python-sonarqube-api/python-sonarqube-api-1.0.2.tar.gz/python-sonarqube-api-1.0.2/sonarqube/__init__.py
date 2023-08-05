#!/usr/bin/env python
# -*- coding:utf-8 -*-
from .exceptions import ClientError, AuthError, ValidationError, ServerError
from .requester import Requester
from .users import SonarQubeUser
from .projects import SonarQubeProject
from .user_groups import SonarQubeUserGroups
from .issues import SonarQubeIssue
from .measures import SonarQubeMeasure
from .notifications import SonarQubeNotification
from .project_links import SonarQubeProjectLinks
from .permissions import SonarQubePermissions
from .ce import SonarQubeCe
from .project_branches import SonarQubeProjectBranches
from .qualitygates import SonarQubeQualityGates
from .components import SonarQubeComponents
from .rules import SonarQubeRules
from .qualityprofiles import SonarQubeQualityprofiles
from .duplications import SonarQubeDuplications
from .metrics import SonarQubeMetrics
from .settings import SonarQubeSettings
from .sources import SonarQubeSources


class SonarQubeClient:
    """
    A Python Client for SonarQube Server APIs.
    """
    DEFAULT_URL = "http://localhost:9000"

    def __init__(self,
                 sonarqube_url=None,
                 username=None,
                 password=None,
                 token=None,
                 ssl_verify=True,
                 cert=None,
                 timeout=10,
                 max_retries=None):
        self._sonarqube_url = self.strip_trailing_slash(sonarqube_url or self.DEFAULT_URL)

        if token:
            self.requester = Requester(
                token,
                baseurl=sonarqube_url,
                ssl_verify=ssl_verify,
                cert=cert,
                timeout=timeout,
                max_retries=max_retries,
            )
        elif username and password:
            self.requester = Requester(
                username,
                password,
                baseurl=sonarqube_url,
                ssl_verify=ssl_verify,
                cert=cert,
                timeout=timeout,
                max_retries=max_retries,
            )

    @classmethod
    def strip_trailing_slash(cls, url):
        """
        remove url's trailing slash
        :param url:
        :return:
        """
        while url.endswith('/'):
            url = url[:-1]
        return url

    def __str__(self):
        return '{}'.format(self._sonarqube_url)

    def _get_url(self, endpoint):
        """
        Return the complete url including host and port for a given endpoint.

        :param endpoint: service endpoint as str
        :return: complete url (including host and port) as str
        """
        return '{}{}'.format(self._sonarqube_url, endpoint)

    def make_call(self, method, endpoint, **data):
        """
        Make the call to the service with the given method, queryset and data,
        using the initial session.

        Note: data is not passed as a single dictionary for better testability
        (see https://github.com/kako-nawao/python-sonarqube-api/issues/15).

        :param method: http method (get, post, put, patch)
        :param endpoint: relative url to make the call
        :param data: queryset or body
        :return: response
        """
        call = getattr(self.requester, method.lower())
        base_url = self._get_url(endpoint)
        res = call(base_url, params=data or {})
        # Analyse response status and return or raise exception
        # Note: redirects are followed automatically by requests
        if res.status_code < 300:
            # OK, return http response
            return res

        elif res.status_code == 400:
            # Validation error
            msg = ', '.join(e['msg'] for e in res.json()['errors'])
            raise ValidationError(msg)

        elif res.status_code in (401, 403):
            # Auth error
            raise AuthError(res.reason)

        elif res.status_code < 500:
            # Other 4xx, generic client error
            raise ClientError(res.reason)

        else:
            # 5xx is server error
            raise ServerError(res.reason)

    @property
    def users(self):
        return SonarQubeUser(self)

    @property
    def user_groups(self):
        return SonarQubeUserGroups(self)

    @property
    def projects(self):
        return SonarQubeProject(self)

    @property
    def measures(self):
        return SonarQubeMeasure(self)

    @property
    def issues(self):
        return SonarQubeIssue(self)

    @property
    def notifications(self):
        return SonarQubeNotification(self)

    @property
    def project_links(self):
        return SonarQubeProjectLinks(self)

    @property
    def permissions(self):
        return SonarQubePermissions(self)

    @property
    def ce(self):
        return SonarQubeCe(self)

    @property
    def project_branches(self):
        return SonarQubeProjectBranches(self)

    @property
    def qualitygates(self):
        return SonarQubeQualityGates(self)

    @property
    def components(self):
        return SonarQubeComponents(self)

    @property
    def rules(self):
        return SonarQubeRules(self)

    @property
    def qualityprofiles(self):
        return SonarQubeQualityprofiles(self)

    @property
    def duplications(self):
        return SonarQubeDuplications(self)

    @property
    def metrics(self):
        return SonarQubeMetrics(self)

    @property
    def settings(self):
        return SonarQubeSettings(self)

    @property
    def sources(self):
        return SonarQubeSources(self)

    @staticmethod
    def copy_dict(dest, src):
        for k, v in src.items():
            if isinstance(v, dict):
                for dict_k, dict_v in v.items():
                    dest['%s[%s]' % (k, dict_k)] = dict_v
            else:
                dest[k] = v
