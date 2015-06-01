#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'
import requests
import logging
import json
from requests.exceptions import HTTPError
from .. import config

log = logging.getLogger()


class Estados(object):
    """
    Estados from Maps
    """
    def __init__(self):
        """
        Constructor method for Estados Base
        """
        self.geo_url = config.GEO_URL

    def get_estados(self):
        """
        Get JSON with information from all states
        :return:
        """
        url = self.geo_url + '/estados'
        response = requests.get(url=url)
        try:
            response.raise_for_status()
        except HTTPError as e:
            log.error("Error getting estados list\n%s", e)

        return response.json()
