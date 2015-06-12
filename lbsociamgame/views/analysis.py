#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'
import datetime
import logging
import time
import json
import operator
from lbsociam.model.crimes import CrimesBase
from lbsociam.model.lbstatus import StatusBase
from lbsociam.model.dictionary import DictionaryBase
from lbsociam.lib import lda
from requests.exceptions import HTTPError
from pyramid.response import Response
from ..lib import utils
from ..model.request import LBRequest

log = logging.getLogger()


class AnalysisController(LBRequest):
    """
    Abalysis controller page
    """
    def __init__(self, request):
        """
        View constructor for analysis
        :param request: Pyramid request
        """
        super(AnalysisController, self).__init__()
        self.request = request

    def crime_analysis(self):
        """
        View to load crime data
        :return:
        """
        # Get date filters
        start_date = self.request.params.get('start')
        end_date = self.request.params.get('end')

        log.debug("Start date: %s", start_date)
        log.debug("End date: %s", end_date)

        # Get starting date
        if start_date is None:
            return Response("Start date mandatory", status=500)

        if end_date is None:
            end_date_obj = datetime.datetime.now()
            end_date = end_date_obj.strftime("%Y-%m-%d")

        search_url = self.status_base.lbgenerator_rest_url + self.status_base.lbbase.metadata.name + '/doc'
        terms = self.dic_base.get_token_frequency(limit=20)

        return {
            'search_url': search_url,
            'key': self.status_base.gmaps_api_key,
            'terms': terms,
            'start_date': start_date,
            'end_date': end_date
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

        # Here explicitly load training base
        saida = lda.crime_topics(
            self.training_base,
            self.crimes_base,
            n_topics
        )

        return saida

    def crime_locations(self):
        """
        Get crimes with locations included
        """
        # Get date filters
        start_date = self.request.params.get('start')
        end_date = self.request.params.get('end')

        # Get starting date
        if start_date is None:
            return Response("Start date mandatory", status=500)
        else:
            start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")

        # Get end date
        if end_date is None:
            end_date_obj = datetime.datetime.now()
            end_date = end_date_obj.strftime("%Y-%m-%d")
        else:
            end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        status_locations = self.status_base.get_locations(
            start_date=start_date_obj,
            end_date=end_date_obj
        )

        # Get training base
        training_base = self.training_base

        # Now find category
        i = 0
        for status in status_locations['results']:
            if status.get('category') is not None:
                category = utils.get_category_id(status['category']['category_id_doc'])
            elif status.get('events_tokens') is not None:
                category = utils.get_category_lda(status, training_base)
            else:
                category = utils.get_category([status['search_term']])

            # Update dict with recently found category
            if category is None:
                log.error("Category not found for status %s\nSearch term: %s",
                          status['_metadata']['id_doc'], status['search_term'])

            status_locations['results'][i]['category'] = category

            # JSON to dict in source
            status_locations['results'][i]['source'] = json.loads(status['source'])

            i += 1

        return {
            'status': status_locations
        }

    def crime_hashtags(self):
        """
        Generate hashtag clouds
        """
        # Get date filters
        start_date = self.request.params.get('start')
        end_date = self.request.params.get('end')

        # Get starting date
        if start_date is None:
            return Response("Start date mandatory", status=500)
        else:
            start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")

        # Get end date
        if end_date is None:
            end_date_obj = datetime.datetime.now()
            end_date = end_date_obj.strftime("%Y-%m-%d")
        else:
            end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        # Number of elements to be in hashtags by default
        n = self.request.params.get('n')
        if n is None:
            n = 50
        else:
            n = int(n)

        log.debug("HASHTAGS: processing starting at %s", time.ctime())
        status = self.status_base.get_hashtags(
            start_date=start_date_obj,
            end_date=end_date_obj
        )

        hashtags = dict()
        for elm in status['results']:
            if elm is not None:
                for elm_hashtag in elm['hashtags']:
                    # Calculate hashtag frequency
                    if hashtags.get(elm_hashtag) is not None:
                        hashtags[elm_hashtag] += 1
                    else:
                        hashtags[elm_hashtag] = 1

        # Ordering results and selecting first 20
        sorted_tags = dict(sorted(hashtags.items(), key=lambda x: x[1], reverse=True)[:n])

        log.debug("HASHTAGS: processing over at %s", time.ctime())

        return {'hashtags': sorted_tags}

    def crime_hashtag_analysis(self):
        """
        Análise da hashtag
        """
        hashtag = self.request.matchdict('hashtag')
        return {}

    def crime_periods(self):
        """
        Hashtags list for the period
        """
        id_doc = self.request.matchdict.get('id_doc')
        analytics = self.analytics_base.get_document(id_doc)

        # Get date filters
        start_date = datetime.datetime.strptime(analytics['analysis_date'], "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%d")
        end_date = datetime.datetime.strptime(analytics['analysis_end_date'], "%d/%m/%Y %H:%M:%S").strftime("%Y-%m-%d")

        # Get starting date
        if start_date is None:
            return Response("Start date mandatory", status=500)
        else:
            start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")

        # Get end date
        if end_date is None:
            end_date_obj = datetime.datetime.now()
            end_date = end_date_obj.strftime("%Y-%m-%d")
        else:
            end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        # Get topics
        n_topics = self.request.params.get('n_topics')
        if n_topics is None:
            # TODO: Get this value from crimes taxonomy base
            n_topics = 4
        else:
            n_topics = int(n_topics)

        # Here explicitly load training base
        topics = lda.crime_topics(
            self.training_base,
            self.crimes_base,
            n_topics
        )

        # Most frequent terms
        terms = self.dic_base.get_token_frequency(limit=5)

        return {
            'start_date': start_date,
            'end_date': end_date,
            'topics': topics,
            'terms': terms
        }
