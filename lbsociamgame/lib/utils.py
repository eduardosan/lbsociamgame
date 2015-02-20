#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import json
import logging
from lbsociam.model.corpus import EventsCorpus
from lbsociam.model.crimes import CrimesBase
from beaker.cache import cache_region
from gensim.models import ldamodel

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
def get_category(tokens, n_topics=4):
    """
    Get category based on supplied tokens list
    :param tokens: Tokens list
    :param n_topics: Number of topics for LDA
    :return: category dict or None
    """
    crimes_base = CrimesBase()

    # Create LDA
    c = get_events_corpus()
    lda = get_lda(n_topics, c)
    topics_list = lda.show_topics(num_topics=n_topics, formatted=False)

    # Now find out the category for this status
    vec_bow = c.dic.doc2bow(tokens)
    vec_lda = lda[vec_bow]

    # Sort by probability
    vec_lda = sorted(vec_lda, key=lambda item: -item[1])

    # Get topic with highest probability
    # It will the first element in vector LDA
    topic = topics_list[vec_lda[0][0]]

    for probability, token_elm in topic:
        category = crimes_base.get_token_by_name(token_elm, full_search=True)
        if category is not None:
            # WE just found the category. Return it
            category['probability'] = probability

            return category

    # If we got here, category was not found
    log.error("Category not found for tokens %s", tokens)

    return None