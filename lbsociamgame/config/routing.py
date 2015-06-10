#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

from lbsociamgame.views import crime, status, analysis, embed, maps, graphics


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

    cfg.add_route('crime_delete', 'crime/delete/{id_doc}')
    cfg.add_view(crime.CrimeController, attr='crime_delete', route_name='crime_delete',
                 request_method='DELETE', renderer='json')

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

    cfg.add_route('status_bulk', 'status/bulk')
    cfg.add_view(status.StatusController, attr='status_bulk', route_name='status_bulk',
                 renderer='templates/status_bulk.pt')

    cfg.add_route('status_up', 'status/up/{id}')
    cfg.add_view(status.StatusController, attr='status_up', route_name='status_up',
                 request_method='POST')

    cfg.add_route('status_down', 'status/down/{id}')
    cfg.add_view(status.StatusController, attr='status_down', route_name='status_down',
                 request_method='POST')

    # Violence and criminality
    cfg.add_route('crime_analysis', 'analysis/crime')
    cfg.add_view(analysis.AnalysisController, attr='crime_analysis',
                 route_name='crime_analysis', renderer='templates/analysis/crime.pt')

    cfg.add_route('crime_topics', 'analysis/crime/topics')
    cfg.add_view(analysis.AnalysisController, attr='crime_topics', route_name='crime_topics',
                 request_method='GET', renderer='json')

    cfg.add_route('crime_locations', 'analysis/crime/locations')
    cfg.add_view(analysis.AnalysisController, attr='crime_locations', route_name='crime_locations',
                 request_method='GET', renderer='json')

    cfg.add_route('twitter_embed', 'embed/twitter/{status_id}')
    cfg.add_view(embed.EmbedController, attr='twitter_embed', route_name='twitter_embed',
                 request_method='GET', renderer='templates/embed/twitter.pt')

    cfg.add_route('crime_hashtags', 'analysis/crime/hashtags')
    cfg.add_view(analysis.AnalysisController, attr='crime_hashtags', route_name='crime_hashtags',
                 request_method='GET', renderer='templates/analysis/hashtags.pt')

    cfg.add_route('crime_hashtag_analysis', 'analysis/crime/hashtags/{hashtag}')
    cfg.add_view(analysis.AnalysisController, attr='crime_hashtag_analysis', route_name='crime_hashtag_analysis',
                 request_method='GET', renderer='templates/analysis/hashtag_analysis.pt')

    cfg.add_route('crime_periods', 'analysis/crime/periods')
    cfg.add_view(analysis.AnalysisController, attr='crime_periods',
                 route_name='crime_periods', renderer='templates/analysis/crime_periods.pt')

    # States map
    cfg.add_route('maps_estados', 'maps/estados')
    cfg.add_view(maps.MapsController, attr='maps_estados',
                 route_name='maps_estados', renderer='templates/maps/estados.pt')

    cfg.add_route('get_estados', 'maps/estados/get')
    cfg.add_view(maps.MapsController, attr='get_estados', route_name='get_estados',
                 request_method='GET', renderer='json')

    # Graphics
    cfg.add_route('category', 'graphics/category/{id_doc}')
    cfg.add_view(graphics.GraphicsController, attr='category',
                 route_name='category', renderer='templates/graphics/category.pt')

    cfg.add_route('category_list', 'graphics/category')
    cfg.add_view(graphics.GraphicsController, attr='category_list',
                 route_name='category_list', renderer='templates/graphics/category_list.pt')

    cfg.add_route('states', 'graphics/states')
    cfg.add_view(graphics.GraphicsController, attr='states',
                 route_name='states', renderer='templates/graphics/states.pt')
