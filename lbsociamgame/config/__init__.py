#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'


def setup(settings):

    global REST_URL
    global GEO_URL

    REST_URL = settings['rest_url']
    GEO_URL = settings['geo_url']
