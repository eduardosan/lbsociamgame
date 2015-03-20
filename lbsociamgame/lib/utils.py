#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import json
import logging
from lbsociam.model.corpus import EventsCorpus
from lbsociam.model.corpus import CategoriesCorpus
from lbsociam.model.crimes import CrimesBase
from beaker.cache import cache_region
from gensim.models import ldamodel
from gensim import similarities

log = logging.getLogger()


def json_load_expression(string):
    """
    JSON dump the string
    :param string: String to be converted
    :return: dict type with data
    """

    return json.loads(string)


@cache_region('long_term')
def get_events_corpus():
    """
    Get cached events corpus
    :return: EventsCorpus object instance
    """
    c = EventsCorpus()
    return c


@cache_region('long_term')
def get_lda(n_topics, corpus):
    """
    Get LDA model
    :param n_topics: Number of topics to use in model
    :param corpus: Corpus object
    :return: LDA model
    """
    lda = ldamodel.LdaModel(corpus.corpus, id2word=corpus.dic, num_topics=n_topics)
    return lda


@cache_region('long_term')
def get_categories_corpus():
    """
    Get cached categories corpus
    :return: CategoriesCorpus object instance
    """
    c = CategoriesCorpus()
    return c


@cache_region('long_term')
def get_index(model, corpus):
    """
    Get similarity index for model and corpus
    :param model: Model to use in similarity, such as LDA os LSI
    :param corpus: Corpus to be used on queries
    :return: MatrixSimilarity instance
    """
    index = similarities.MatrixSimilarity(model[corpus])
    return index


@cache_region('long_term')
def get_category(tokens):
    """
    Get category based on supplied tokens list
    :param tokens: Tokens list
    :return: category dict or None
    """
    crimes_base = CrimesBase()

    for elm in tokens:
        category = crimes_base.get_token_by_name(elm)
        if category is not None:
            log.debug("Token %s found!", elm)
            return category