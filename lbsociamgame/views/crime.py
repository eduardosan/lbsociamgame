#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import logging
import datetime
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer
from pyramid.httpexceptions import HTTPFound
from lbsociamgame.model import crime as crime_schema
from lbsociam.model.crimes import Crimes, CrimesBase

log = logging.getLogger()


class CrimeController(object):
    """
    Crime controller
    """
    def __init__(self, request):
        """
        View constructor for crimes
        :param request: Pyramid request
        """
        self.request = request

    def crime_add(self):
        """
        Crimes list for classification
        :return:
        """
        # Gera formulário
        form = Form(self.request,
                    defaults={},
                    schema=crime_schema.CrimeSchema())

        if form.validate():
            log.debug("Dados do formulário: ")

            # Tenta instanciar o formulário no objeto
            crime_obj = Crimes(
                category_name=self.request.params.get('category_name'),
                category_pretty_name=self.request.params.get('category_pretty_name'),
                description=self.request.params.get('description'),
                date=datetime.datetime.now()
            )

            # persist model somewhere...
            crime_obj.create_crimes()

            return HTTPFound(location="/crime")

        return dict(renderer=FormRenderer(form))

    def crimes(self):
        """
        Crimes list
        """
        crimes_base = CrimesBase()
        results = crimes_base.list()

        return {
            'results': results
        }