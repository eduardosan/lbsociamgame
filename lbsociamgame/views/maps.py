#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'
import logging
import json
from ..model.request import LBRequest

log = logging.getLogger()

class MapsController(LBRequest):
    """
    Controller for some special maps
    """
    def __init__(self, request):
        """
        View constructor for request
        :param request:  Pyramid request
        """
        super(MapsController, self).__init__()
        self.request = request

    def get_estados(self):
        """
        Pega lista de todos os estados
        """
        return self.estados.get_estados()

    def maps_estados(self):
        """
        Map with all estados from Brasil
        """
        url = self.estados.geo_url + '/estados'
        return {
            'estados': url,
            'key': self.status_base.gmaps_api_key,
        }
