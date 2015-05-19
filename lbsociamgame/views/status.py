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
from ..lib import utils
from ..model.request import LBRequest

log = logging.getLogger()


class StatusController(LBRequest):
    """
    Crime controller
    """
    def __init__(self, request):
        """
        View constructor for crimes
        :param request: Pyramid request
        """
        super(StatusController, self).__init__()
        self.request = request

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

    def status_bulk(self):
        """
        Bulk classificate status
        """
        limit = 50
        page = self.request.params.get('page')
        if page is None:
            offset = 0
            page = 1
        else:
            offset = (int(page) - 1) * limit
            page = int(page)

        # Get only documents with identified events
        literal = "json_array_length((document->>'events_tokens')::json) > 0"
        collection = self.status_base.get_status(
            limit=limit,
            offset=offset,
            literal=literal
        )

        total_pages = (int(collection['result_count']) // limit) + 1
        last_page = page + 6
        if total_pages < last_page:
            last_page = total_pages

        return {
            'status_collection': collection,
            'last_page': last_page,
            'page': page
        }

    def status_up(self):
        """
        Positive evaluation for status
        :return:
        """
        id_doc = self.request.matchdict['id']
        try:
            positives = int(self.status_base.documentrest.get_path(id_doc, ['positives']))
        except HTTPError:
            positives = 0

        # add 1 on positive evaluations
        positives += 1

        response = Response(content_type='application/json')

        # Update on base
        result = self.status_base.documentrest.update_path(id_doc, ['positives'], positives)
        response.status_code = 200
        response.text = result

        return response

    def status_down(self):
        """
        Positive evaluation for status
        :return:
        """
        id_doc = self.request.matchdict['id']
        try:
            negatives = int(self.status_base.documentrest.get_path(id_doc, ['negatives']))
        except HTTPError:
            negatives = 0

        # add 1 on positive evaluations
        negatives += 1

        response = Response(content_type='application/json')

        # Update on base
        result = self.status_base.documentrest.update_path(id_doc, ['negatives'], negatives)
        response.status_code = 200
        response.text = result

        return response