#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import logging
import time
import json
from lbsociam.model.crimes import CrimesBase
from lbsociam.model.lbstatus import StatusBase
from lbsociam.model.corpus import EventsCorpus
from lbsociam.model.dictionary import DictionaryBase
from lbsociam.model.lbtwitter import Twitter
from gensim.models import ldamodel
from requests.exceptions import HTTPError
from pyramid.response import Response
from liblightbase.lbutils import conv
from pyramid.exceptions import HTTPBadRequest
from ..lib import utils

log = logging.getLogger()


class EmbedController(object):
    """
    Abalysis controller page
    """
    def __init__(self, request):
        """
        View constructor for analysis
        :param request: Pyramid request
        """
        self.request = request
        self.crimes_base = CrimesBase()
        self.status_base = StatusBase()
        self.dic_base = DictionaryBase()
        self.lbt = Twitter()

    def twitter_embed(self):
        """
        View for twitter embed

        :return: Twitter HTML code with oEmbed
        """
        status_id = self.request.matchdict.get('status_id')
        if status_id is None:
            log.error("You have to supply status_id")
            raise HTTPError

        status = self.status_base.get_document(status_id)
        status_dict = conv.document2dict(self.status_base.lbbase, status)
        status_dict['_metadata'] = dict()
        status_dict['_metadata']['id_doc'] = status_id

        # Load original source
        source = json.loads(status_dict['source'])
        status_dict['source'] = source[0]

        # Get status oembed
        oembed = self.lbt.api.GetStatusOembed(id=status_dict['source']['_id'], lang='pt')

        # Get category
        if status_dict.get('events_tokens') is None:
            status_dict['category'] = utils.get_category(status_dict['events_tokens'])
        else:
            status_dict['category'] = utils.get_category([status_dict['search_term']])

        return {
            'oembed_html': oembed['html'],
            'status': status_dict
        }