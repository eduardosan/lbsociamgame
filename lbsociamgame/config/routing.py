#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

from lbsociamgame.views import crime, status


def make_routes(cfg):
    """
    Create module routes
    :param cfg: Configurator object
    """
    cfg.add_static_view('static', 'static', cache_max_age=3600)
    cfg.add_route('home', '/')

    # Crime classification routes
    cfg.add_route('crime_add', 'crime/new')
    cfg.add_view(crime.CrimeController, attr='crime_add', route_name='crime_add',
                 renderer='templates/crime_add.pt')

    cfg.add_route('crime_edit', 'crime/{id_doc}')
    cfg.add_view(crime.CrimeController, attr='crime_edit', route_name='crime_edit',
                 renderer='templates/crime_add.pt')

    # Crime classification routes
    cfg.add_route('crimes', 'crime')
    cfg.add_view(crime.CrimeController, attr='crimes', route_name='crimes',
                 renderer='templates/crimes.pt')

    cfg.add_route('images', 'crime/{id_doc}/images')
    cfg.add_view(crime.CrimeController, attr='images', route_name='images',
                 renderer='templates/crime_images.pt')

    cfg.add_route('insert_images', 'crime/{id_doc}/images/upload', request_method='POST')
    cfg.add_view(crime.CrimeController, attr='insert_images', route_name='insert_images')

    cfg.add_route('remove_image', 'crime/{id_doc}/images/{id_file}', request_method='DELETE')
    cfg.add_view(crime.CrimeController, attr='remove_image', route_name='remove_image')

    # Status routes
    cfg.add_route('status_class', 'status/class/{id_doc}')
    cfg.add_view(status.StatusController, attr='status_class', route_name='status_class',
                 renderer='templates/status_class.pt')

    # Status routes
    cfg.add_route('status_category', 'status/class/{id_doc}/{id_cat}', request_method='POST')
    cfg.add_view(status.StatusController, attr='status_category', route_name='status_category')