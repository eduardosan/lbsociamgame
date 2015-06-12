__author__ = 'eduardo'

from lbsociam.model.crimes import CrimesBase
from lbsociam.model.lbstatus import StatusBase
from lbsociam.model.dictionary import DictionaryBase
from lbsociam.model.lbtwitter import Twitter
from lbsociam.model.analytics import AnalyticsBase
from ..model.estados import Estados

class LBRequest(object):
    """
    Basic attributes for every request
    """

    def __init__(self):
        """
        Constructor method to load basic attributes
        """
        self.crimes_base = CrimesBase()
        self.status_base = StatusBase(
            status_name='status',
            dic_name='dictionary'
        )
        self.dic_base = DictionaryBase(
            dic_base='dictionary'
        )
        self.lbt = Twitter()
        self.training_base = StatusBase()
        self.estados = Estados()
        self.analytics_base = AnalyticsBase(
            self.status_base
        )
