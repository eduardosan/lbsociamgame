#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

from formencode import Schema, validators


class CrimeSchema(Schema):
    """
    Crime Form schema
    """

    allow_extra_fields = True
    filter_extra_fields = True

    category_name = validators.UnicodeString()
    category_pretty_name = validators.UnicodeString()
    description = validators.UnicodeString()


class ImageSchema(Schema):
    """
    Schema for image upload
    """
    allow_extra_fields = True
    filter_extra_fields = True

    image = validators.FieldStorageUploadConverter()