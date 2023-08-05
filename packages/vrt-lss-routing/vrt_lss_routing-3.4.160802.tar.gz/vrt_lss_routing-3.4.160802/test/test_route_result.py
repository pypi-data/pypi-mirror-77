# coding: utf-8

"""
    VeeRoute.LSS Routing

    VeeRoute.LSS Routing API  # noqa: E501

    The version of the OpenAPI document: 3.4.160802
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import vrt_lss_routing
from vrt_lss_routing.models.route_result import RouteResult  # noqa: E501
from vrt_lss_routing.rest import ApiException

class TestRouteResult(unittest.TestCase):
    """RouteResult unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test RouteResult
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_routing.models.route_result.RouteResult()  # noqa: E501
        if include_optional :
            return RouteResult(
                tracedata = vrt_lss_routing.models.trace_data.TraceData(
                    code = 'client_server_service_time_id', ), 
                route = vrt_lss_routing.models.route.Route(
                    legs = [
                        vrt_lss_routing.models.route_leg.RouteLeg(
                            steps = [
                                vrt_lss_routing.models.route_step.RouteStep(
                                    transport_type = 'CAR', 
                                    polyline = vrt_lss_routing.models.route_polyline.RoutePolyline(
                                        points = [
                                            vrt_lss_routing.models.waypoint.Waypoint(
                                                name = 'central', 
                                                latitude = 55.692789, 
                                                longitude = 37.554554, 
                                                duration = 15, )
                                            ], ), )
                                ], 
                            statistics = vrt_lss_routing.models.route_statistics.RouteStatistics(
                                distance = 7000, 
                                duration = 60, 
                                stopping_time = 20, 
                                time_window = vrt_lss_routing.models.route_statistics_time_window.RouteStatistics_time_window(
                                    from = '2020-10-21T09:30+03:00', 
                                    to = '2020-10-21T19:45Z', ), ), )
                        ], 
                    statistics = vrt_lss_routing.models.route_statistics.RouteStatistics(
                        distance = 7000, 
                        duration = 60, 
                        stopping_time = 20, ), )
            )
        else :
            return RouteResult(
                route = vrt_lss_routing.models.route.Route(
                    legs = [
                        vrt_lss_routing.models.route_leg.RouteLeg(
                            steps = [
                                vrt_lss_routing.models.route_step.RouteStep(
                                    transport_type = 'CAR', 
                                    polyline = vrt_lss_routing.models.route_polyline.RoutePolyline(
                                        points = [
                                            vrt_lss_routing.models.waypoint.Waypoint(
                                                name = 'central', 
                                                latitude = 55.692789, 
                                                longitude = 37.554554, 
                                                duration = 15, )
                                            ], ), )
                                ], 
                            statistics = vrt_lss_routing.models.route_statistics.RouteStatistics(
                                distance = 7000, 
                                duration = 60, 
                                stopping_time = 20, 
                                time_window = vrt_lss_routing.models.route_statistics_time_window.RouteStatistics_time_window(
                                    from = '2020-10-21T09:30+03:00', 
                                    to = '2020-10-21T19:45Z', ), ), )
                        ], 
                    statistics = vrt_lss_routing.models.route_statistics.RouteStatistics(
                        distance = 7000, 
                        duration = 60, 
                        stopping_time = 20, ), ),
        )

    def testRouteResult(self):
        """Test RouteResult"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
