#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'

from pyramid.view import view_config


@view_config(route_name='home', renderer='../templates/mytemplate.pt')
def my_view(request):
    return {'project': 'lbsociamgame'}
