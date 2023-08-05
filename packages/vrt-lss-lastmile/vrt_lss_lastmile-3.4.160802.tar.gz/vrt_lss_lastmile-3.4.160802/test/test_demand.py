# coding: utf-8

"""
    VeeRoute.LSS Lastmile

    VeeRoute.LSS Lastmile API  # noqa: E501

    The version of the OpenAPI document: 3.4.160802
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import vrt_lss_lastmile
from vrt_lss_lastmile.models.demand import Demand  # noqa: E501
from vrt_lss_lastmile.rest import ApiException

class TestDemand(unittest.TestCase):
    """Demand unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test Demand
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_lastmile.models.demand.Demand()  # noqa: E501
        if include_optional :
            return Demand(
                key = 'demand_1', 
                demand_type = 'WORK', 
                target_cargos = ["cargo01"], 
                precedence_in_trip = 1, 
                precedence_in_order = 1, 
                possible_events = [
                    vrt_lss_lastmile.models.possible_event.PossibleEvent(
                        location_key = 'location01', 
                        duration = 10, 
                        reward = 199.9, 
                        time_window = vrt_lss_lastmile.models.time_window.TimeWindow(
                            from = '2020-10-21T09:30+03:00', 
                            to = '2020-10-21T19:45Z', ), 
                        soft_time_window = vrt_lss_lastmile.models.time_window.TimeWindow(
                            from = '2020-10-21T09:30+03:00', 
                            to = '2020-10-21T19:45Z', ), )
                    ]
            )
        else :
            return Demand(
                key = 'demand_1',
                demand_type = 'WORK',
                possible_events = [
                    vrt_lss_lastmile.models.possible_event.PossibleEvent(
                        location_key = 'location01', 
                        duration = 10, 
                        reward = 199.9, 
                        time_window = vrt_lss_lastmile.models.time_window.TimeWindow(
                            from = '2020-10-21T09:30+03:00', 
                            to = '2020-10-21T19:45Z', ), 
                        soft_time_window = vrt_lss_lastmile.models.time_window.TimeWindow(
                            from = '2020-10-21T09:30+03:00', 
                            to = '2020-10-21T19:45Z', ), )
                    ],
        )

    def testDemand(self):
        """Test Demand"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
