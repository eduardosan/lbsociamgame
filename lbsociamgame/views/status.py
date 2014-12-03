#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import logging
import datetime
import requests
import json
import random
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer
from pyramid.httpexceptions import HTTPFound, HTTPBadRequest
from pyramid.response import Response
from lbsociamgame.model import crime as crime_schema
from lbsociam.model.crimes import Crimes, CrimesBase
from lbsociam.model.lbstatus import Status, StatusBase
from liblightbase.lbutils import conv
from liblightbase.lbtypes import extended
from requests.exceptions import HTTPError

log = logging.getLogger()


class StatusController(object):
    """
    Crime controller
    """
    def __init__(self, request):
        """
        View constructor for crimes
        :param request: Pyramid request
        """
        self.request = request
        self.crimes_base = CrimesBase()
        self.status_base = StatusBase()

    def status_class(self):
        """
        Status general classification view
        """
        # FIXME: Por enquanto utiliza um número aleatório para visualizar
        base_json = self.status_base.get_base()
        max_results = int(base_json['result_count'])
        id_doc = self.request.matchdict['id_doc']
        if id_doc is None:
            id_doc = random.randint(1, max_results)

        # Try to get this status
        status = None
        try:
            status = self.status_base.documentrest.get(id_doc)
            status.source = json.loads(status.source)
        except HTTPError as e:
            # Try to get another document
            log.debug("Document not found: %s", id_doc)
            if self.request.matchdict['id_doc'] is None:
                self.status_class()

        #log.debug(status.source[0]['_user']['_profile_image_url'])
        # Agora pega dados dos crimes
        crimes = self.crimes_base.list()
        log.debug(crimes['results'])

        return {
            'status': status,
            'crimes': crimes['results'],
            'rest_url': self.crimes_base.lbgenerator_rest_url + '/' + self.crimes_base.lbbase._metadata.name,
            'id_doc': id_doc
        }

    def status_category(self):
        """
        Add status tokens to category
        """
        id_status = self.request.matchdict['id_doc']
        id_cat = self.request.matchdict['id_cat']

        status = self.status_base.get_document(id_status)
        category = self.crimes_base.get_document(id_cat)

        if category.get('tokens') is None:
            category['tokens'] = status.tokens
        else:
            category['tokens'] = category['tokens'] + status.tokens
            category['tokens'] = list(set(category['tokens']))

        response = self.crimes_base.update_document(id_cat, category)

        return response