#!/usr/env python
# -*- coding: utf-8 -*-
__author__ = 'eduardo'
import logging
import datetime
from pyramid.request import Response
from ..model.request import LBRequest
import plotly.plotly as py
from plotly.graph_objs import *

log = logging.getLogger()


class GraphicsController(LBRequest):
    """
    Abalysis controller page
    """
    def __init__(self, request):
        """
        View constructor for analysis
        :param request: Pyramid request
        """
        super(GraphicsController, self).__init__()
        self.request = request

    def category(self):
        """
        Probability histogram for category
        """
        id_doc = self.request.matchdict.get('id_doc')
        start_date = self.request.params.get('start_date')
        end_date = self.request.params.get('end_date')

        # Get starting date
        if start_date is None:
            return Response("Start date mandatory", status=500)
        else:
            start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")

        # Get end date
        if end_date is None:
            end_date_obj = datetime.datetime.now()
            end_date = end_date_obj.strftime("%Y-%m-%d")
        else:
            end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        status_list = self.status_base.get_status_probability(
            category_id_doc=id_doc,
            start_date=start_date_obj,
            end_date=end_date_obj
        )

        if len(status_list) == 0:
            return {}

        # Transform results in list of values
        saida = list()
        for status in status_list['results']:
            if status is not None:
                saida.append(status['category']['category_probability'])

        # Plot Histogram
        data = Data([
            Histogram(
                x=saida
            )
        ])

        filename = "category-" + id_doc + "-" + start_date + "-" + end_date
        plot_url = py.plot(data, filename=filename)

        return {
            "graph_url": plot_url,
            "category_id_doc": id_doc
        }

    def category_list(self):
        """
        Probability histogram for category
        """
        start_date = self.request.params.get('start_date')
        end_date = self.request.params.get('end_date')

        # Get starting date
        if start_date is None:
            return Response("Start date mandatory", status=500)
        else:
            start_date_obj = datetime.datetime.strptime(start_date, "%Y-%m-%d")

        # Get end date
        if end_date is None:
            end_date_obj = datetime.datetime.now()
            end_date = end_date_obj.strftime("%Y-%m-%d")
        else:
            end_date_obj = datetime.datetime.strptime(end_date, "%Y-%m-%d")

        categories = self.crimes_base.get_all()

        graph_list = list()
        for category in categories:
            id_doc = category['_metadata']['id_doc']
            # Render all categories
            status_list = self.status_base.get_status_probability(
                category_id_doc=id_doc,
                start_date=start_date_obj,
                end_date=end_date_obj
            )

            if len(status_list) == 0:
                return {}

            # Transform results in list of values
            saida = list()
            for status in status_list['results']:
                if status is not None:
                    saida.append(status['category']['category_probability'])

            # Plot Histogram
            graph = Histogram(
                x=saida,
                opacity=0.75,
                name=category['category_pretty_name'],
                xbins=XBins(
                    # start=-3.2,
                    # end=2.8,
                    # size=0.2
                ),
                marker=Marker(
                    color=category['color']
                ),
            )

            graph_list.append(graph)

        data = Data(graph_list)
        layout = Layout(
            title="""Probabilidade na Categoria entre %s e %s""" % (start_date, end_date),
            xaxis=XAxis(
                title='Probabilidade'
            ),
            yaxis=YAxis(
                title='Ocorrências'
            ),
            barmode='overlay',
            # bargap=0.25,
            # bargroupgap=0.3
        )

        filename = "category-" + start_date + "-" + end_date
        fig = Figure(data=data, layout=layout)
        plot_url = py.plot(fig, filename=filename)

        return {
            'graph_url': plot_url,
            'graph_id': filename
        }
