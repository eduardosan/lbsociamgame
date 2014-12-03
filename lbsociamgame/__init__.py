#!/usr/env python
# -*- coding: utf-8 -*-
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from lbsociamgame import config as cfg
from lbsociam import config as lbconfig


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    cfg.setup(settings)

    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')

    # Session configuration
    config.include('pyramid_beaker')
    my_session_factory = SignedCookieSessionFactory(settings['session.secret'])
    config.set_session_factory(my_session_factory)

    # Import routes
    from lbsociamgame.config import routing
    routing.make_routes(config)
    config.scan()

    return config.make_wsgi_app()