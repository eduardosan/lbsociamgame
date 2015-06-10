#!/usr/env python
# -*- coding: utf-8 -*-
import plotly
from pyramid.config import Configurator
from pyramid.session import SignedCookieSessionFactory
from lbsociamgame import config as cfg
from pyramid_beaker import set_cache_regions_from_settings


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    cfg.setup(settings)

    # Load cache config
    set_cache_regions_from_settings(settings)

    config = Configurator(settings=settings)
    config.include('pyramid_chameleon')

    # Session configuration
    config.include('pyramid_beaker')
    my_session_factory = SignedCookieSessionFactory(settings['session.secret'])
    config.set_session_factory(my_session_factory)

    # Get plotly credentials
    plotly.tools.set_credentials_file(
        username=settings['plotly_username'],
        api_key=settings['plotly_key']
    )

    # Import routes
    from lbsociamgame.config import routing
    routing.make_routes(config)
    config.scan()

    return config.make_wsgi_app()
