#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

import logging
import datetime
import requests
import json
from pyramid_simpleform import Form
from pyramid_simpleform.renderers import FormRenderer
from pyramid.httpexceptions import HTTPFound, HTTPBadRequest
from pyramid.response import Response
from lbsociamgame.model import crime as crime_schema
from lbsociam.model.crimes import Crimes, CrimesBase
from liblightbase.lbutils import conv
from liblightbase.lbtypes import extended

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
        self.crimes_base = CrimesBase()

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

        return dict(
            renderer=FormRenderer(form),
            action=self.request.route_url('crime_add')
        )

    def crimes(self):
        """
        Crimes list
        """

        results = self.crimes_base.list()

        return {
            'results': results
        }

    def images(self):
        """
        List related images on category
        """
        crime_document = self.crimes_base.get_document(self.request.matchdict['id_doc'])
        crime_document['__valreq__'] = False

        return {
            'crime_document': crime_document,
            'rest_url': self.crimes_base.lbgenerator_rest_url + '/' + self.crimes_base.lbbase._metadata.name
        }

    def insert_images(self):
        """
        Insert image on document
        :return:
        """
        id_doc = self.request.matchdict.get('id_doc')
        image = self.request.params.get('image')
        if id_doc is None or image is None:
            log.error("id_doc and image required")
            raise HTTPBadRequest

        response = Response(content_type='application/json')

        # Primeiro insere o documento
        result = self.crimes_base.upload_file(image)

        log.info("Status code: %s", result.status_code)

        if result.status_code >= 300:
            log.error("Erro na insercao!\n%s", result.text)
            response.status_code = result.status_code
            response.text = result.text
            return response

        file_dict = json.loads(result.text)
        #file_dict['filename'] = image.filename
        #file_dict['mimetype'] = image.type
        log.debug("UUID para arquivo gerado: %s", file_dict)

        result = self.crimes_base.update_file_document(id_doc, file_dict)

        if result.status_code >= 300:
            log.error("Erro na atualização da imagem %s", result.text)
            response.status_code = 500
            response.text = result.text
            return response

        response.status_code = 200
        response.text = result.text

        return response

    def remove_image(self):
        """
        Remove imagem da base
        """
        # Primeiro recupera o documento
        id_doc = self.request.matchdict.get('id_doc')
        id_file = self.request.matchdict.get('id_file')

        response = self.crimes_base.remove_file(id_doc, id_file)

        return response

    def crime_edit(self):
        """
        Crimes list for classification
        :return:
        """
        # Retrieve id_doc
        id_doc = self.request.matchdict['id_doc']
        crime_dict = self.crimes_base.get_document(id_doc)
        log.debug(crime_dict)

        # Gera formulário
        form = Form(self.request,
                    defaults=crime_dict,
                    schema=crime_schema.CrimeSchema())

        if form.validate():
            log.debug("Dados do formulário: ")

            # Tenta instanciar o formulário no objeto
            crime_obj = Crimes(
                category_name=self.request.params.get('category_name'),
                category_pretty_name=self.request.params.get('category_pretty_name'),
                description=self.request.params.get('description'),
                default_token=self.request.params.get('default_token'),
                date=datetime.datetime.now()
            )

            # persist model somewhere...
            #crime_obj.update(id_doc)

            # Corrige bug das imagens
            crime_up = conv.document2dict(self.crimes_base.lbbase, crime_obj)
            crime_up['images'] = crime_dict.get('images')

            url = self.crimes_base.lbgenerator_rest_url + '/' + self.crimes_base.lbbase.metadata.name + '/doc/' + id_doc
            #log.debug(crime_up)
            params = {
                'value': json.dumps(crime_up)
            }
            response = requests.put(
                url=url,
                data=params
            )

            return HTTPFound(location="/crime")

        return dict(
            renderer=FormRenderer(form),
            action=self.request.route_url(
                'crime_edit',
                id_doc=id_doc
            )
        )