#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import logging
import time
import operator
from lbsociam.model.crimes import CrimesBase
from lbsociam.model.lbstatus import StatusBase
from lbsociam.model.corpus import EventsCorpus
from gensim.models import ldamodel
from requests.exceptions import HTTPError
from pyramid.response import Response

log = logging.getLogger()


class AnalysisController(object):
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

    def crime_analysis(self):
        """
        View to load crime data
        :return:
        """
        search_url = self.status_base.lbgenerator_rest_url + self.status_base.lbbase.metadata.name + '/doc'

        return {
            'search_url': search_url,
            'key': self.status_base.gmaps_api_key
        }

    def crime_topics(self):
        """
        Generate crime topics
        :return: dict with term frequency calculated by LDA
        """
        n_topics = self.request.params.get('n_topics')
        if n_topics is None:
            # TODO: Get this value from crimes taxonomy base
            n_topics = 4
        else:
            n_topics = int(n_topics)

        t0 = time.clock()
        c = EventsCorpus()
        t1 = time.clock() - t0
        log.debug("Time to generate Corpus: %s seconds", t1)

        t0 = time.clock()
        lda = ldamodel.LdaModel(c.corpus, id2word=c.dic, num_topics=n_topics)
        t1 = time.clock() - t0
        log.debug("Time to generate LDA Modelfor %s topics: %s seconds", n_topics, t1)

        topics_list = lda.show_topics(num_topics=n_topics, formatted=False)
        base_info = self.status_base.get_base()
        total_status = int(base_info['result_count'])
        #log.debug(topics_list)

        saida = dict()
        i = 0
        for elm in topics_list:
            saida[i] = list()
            for token in elm:
                probability = token[0]
                word = token[1]
                saida[i].append(dict(
                    word=word,
                    probability=probability,
                    frequency=probability*total_status
                ))

            i += 1

        return saida

    def crime_locations(self):
        """
        Get crimes with locations included
        :return:
        """

        status_locations = self.status_base.get_locations()

        return status_locations