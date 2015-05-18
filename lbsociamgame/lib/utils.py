#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import json
import logging
from lbsociam.model.corpus import EventsCorpus
from lbsociam.model.corpus import CategoriesCorpus
from lbsociam.model.crimes import CrimesBase
from lbsociam.lib import corpus
from lbsociam.lib import lda
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
def get_events_corpus(status_base):
    """
    Get cached events corpus
    :return: EventsCorpus object instance
    """
    return corpus.get_events_corpus(status_base)


@cache_region('long_term')
def get_lda(n_topics, c):
    """
    Get LDA model
    :param n_topics: Number of topics to use in model
    :param corpus: Corpus object
    :return: LDA model
    """
    return lda.get_lda(c, n_topics)


@cache_region('long_term')
def get_categories_corpus(crimes_base):
    """
    Get cached categories corpus
    :return: CategoriesCorpus object instance
    """
    c = CategoriesCorpus(crimes_base=crimes_base)
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


@cache_region('log_term')
def get_category_id(id_doc):
    """
    Get category metadata for the supplied ID

    :param id_doc: ID for the category to use
    :return: Category metadata as dict
    """
    crimes_base = CrimesBase()
    category = crimes_base.get_document(id_doc)

    return category

@cache_region('log_term')
def get_category_lda(status,
                     status_base):
    """
    Get Category for status using LDA model
    :param status: Status dict to be analyzed
    :param status_base: Status base to consider
    :return: Status dict
    """

    crimes_base = CrimesBase()
    status = lda.get_category(
        status,
        status_base,
        crimes_base
    )

    return status