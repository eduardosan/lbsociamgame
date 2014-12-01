#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

from lbsociamgame.views import crime


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

    # Crime classification routes
    cfg.add_route('crimes', 'crime')
    cfg.add_view(crime.CrimeController, attr='crimes', route_name='crimes',
                 renderer='templates/crimes.pt')