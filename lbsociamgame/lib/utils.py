#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import json


def json_load_expression(string):
    """
    JSON dump the string
    :param string: String to be converted
    :return: dict type with data
    """

    return json.loads(string)