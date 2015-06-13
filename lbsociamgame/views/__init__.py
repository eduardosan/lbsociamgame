#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

from pyramid.view import view_config


@view_config(route_name='home', renderer='../templates/home.pt')
def my_view(request):
    return {}

@view_config(route_name="about", renderer='../templates/about.pt')
def about(request):
    return {}
