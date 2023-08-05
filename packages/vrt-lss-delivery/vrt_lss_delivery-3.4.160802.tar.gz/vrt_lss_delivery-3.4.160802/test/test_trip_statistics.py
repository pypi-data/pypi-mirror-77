# coding: utf-8

"""
    VeeRoute.LSS Delivery

    VeeRoute.LSS Delivery API  # noqa: E501

    The version of the OpenAPI document: 3.4.160802
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import vrt_lss_delivery
from vrt_lss_delivery.models.trip_statistics import TripStatistics  # noqa: E501
from vrt_lss_delivery.rest import ApiException

class TestTripStatistics(unittest.TestCase):
    """TripStatistics unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test TripStatistics
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_delivery.models.trip_statistics.TripStatistics()  # noqa: E501
        if include_optional :
            return TripStatistics(
                trip_key = 'trip01', 
                statistics = vrt_lss_delivery.models.statistics.Statistics(
                    cost = 1231.1, 
                    reward = 2343.3, 
                    measurements = vrt_lss_delivery.models.measurements.Measurements(
                        driving_time = 15, 
                        waiting_time = 5, 
                        working_time = 50, 
                        arriving_time = 30, 
                        departure_time = 20, 
                        total_time = 120, 
                        distance = 5200, 
                        time_window = vrt_lss_delivery.models.time_window.TimeWindow(
                            from = '2020-10-21T09:30+03:00', 
                            to = '2020-10-21T19:45Z', ), ), 
                    orders_count = 1700, 
                    performers_count = 257, 
                    capacity_utilization = vrt_lss_delivery.models.capacity.Capacity(
                        mass = 10, 
                        volume = 2, 
                        capacity_x = 1, 
                        capacity_y = 2, 
                        capacity_z = 3, ), 
                    capacity_max = vrt_lss_delivery.models.capacity.Capacity(
                        mass = 10, 
                        volume = 2, 
                        capacity_x = 1, 
                        capacity_y = 2, 
                        capacity_z = 3, ), ), 
                stop_statistics = [
                    vrt_lss_delivery.models.stop_statistics.StopStatistics(
                        location = vrt_lss_delivery.models.location.Location(
                            latitude = 55.692789, 
                            longitude = 37.554554, 
                            arrival_duration = 15, 
                            departure_duration = 5, ), 
                        location_key = 'location01', 
                        demand_ids = [
                            'demand01'
                            ], 
                        measurements = vrt_lss_delivery.models.measurements.Measurements(
                            driving_time = 15, 
                            waiting_time = 5, 
                            working_time = 50, 
                            arriving_time = 30, 
                            departure_time = 20, 
                            total_time = 120, 
                            distance = 5200, 
                            time_window = vrt_lss_delivery.models.time_window.TimeWindow(
                                from = '2020-10-21T09:30+03:00', 
                                to = '2020-10-21T19:45Z', ), ), 
                        upload = vrt_lss_delivery.models.transport_load.TransportLoad(
                            count = 460, 
                            capacity = vrt_lss_delivery.models.capacity.Capacity(
                                mass = 10, 
                                volume = 2, 
                                capacity_x = 1, 
                                capacity_y = 2, 
                                capacity_z = 3, ), ), 
                        download = vrt_lss_delivery.models.transport_load.TransportLoad(
                            count = 460, 
                            capacity = vrt_lss_delivery.models.capacity.Capacity(
                                mass = 10, 
                                volume = 2, 
                                capacity_x = 1, 
                                capacity_y = 2, 
                                capacity_z = 3, ), ), 
                        current_load = vrt_lss_delivery.models.transport_load.TransportLoad(
                            count = 460, 
                            capacity = vrt_lss_delivery.models.capacity.Capacity(
                                mass = 10, 
                                volume = 2, 
                                capacity_x = 1, 
                                capacity_y = 2, 
                                capacity_z = 3, ), ), )
                    ], 
                total_load = vrt_lss_delivery.models.transport_load.TransportLoad(
                    count = 460, 
                    capacity = vrt_lss_delivery.models.capacity.Capacity(
                        mass = 10, 
                        volume = 2, 
                        capacity_x = 1, 
                        capacity_y = 2, 
                        capacity_z = 3, ), ), 
                max_load = vrt_lss_delivery.models.transport_load.TransportLoad(
                    count = 460, 
                    capacity = vrt_lss_delivery.models.capacity.Capacity(
                        mass = 10, 
                        volume = 2, 
                        capacity_x = 1, 
                        capacity_y = 2, 
                        capacity_z = 3, ), )
            )
        else :
            return TripStatistics(
                trip_key = 'trip01',
                statistics = vrt_lss_delivery.models.statistics.Statistics(
                    cost = 1231.1, 
                    reward = 2343.3, 
                    measurements = vrt_lss_delivery.models.measurements.Measurements(
                        driving_time = 15, 
                        waiting_time = 5, 
                        working_time = 50, 
                        arriving_time = 30, 
                        departure_time = 20, 
                        total_time = 120, 
                        distance = 5200, 
                        time_window = vrt_lss_delivery.models.time_window.TimeWindow(
                            from = '2020-10-21T09:30+03:00', 
                            to = '2020-10-21T19:45Z', ), ), 
                    orders_count = 1700, 
                    performers_count = 257, 
                    capacity_utilization = vrt_lss_delivery.models.capacity.Capacity(
                        mass = 10, 
                        volume = 2, 
                        capacity_x = 1, 
                        capacity_y = 2, 
                        capacity_z = 3, ), 
                    capacity_max = vrt_lss_delivery.models.capacity.Capacity(
                        mass = 10, 
                        volume = 2, 
                        capacity_x = 1, 
                        capacity_y = 2, 
                        capacity_z = 3, ), ),
                stop_statistics = [
                    vrt_lss_delivery.models.stop_statistics.StopStatistics(
                        location = vrt_lss_delivery.models.location.Location(
                            latitude = 55.692789, 
                            longitude = 37.554554, 
                            arrival_duration = 15, 
                            departure_duration = 5, ), 
                        location_key = 'location01', 
                        demand_ids = [
                            'demand01'
                            ], 
                        measurements = vrt_lss_delivery.models.measurements.Measurements(
                            driving_time = 15, 
                            waiting_time = 5, 
                            working_time = 50, 
                            arriving_time = 30, 
                            departure_time = 20, 
                            total_time = 120, 
                            distance = 5200, 
                            time_window = vrt_lss_delivery.models.time_window.TimeWindow(
                                from = '2020-10-21T09:30+03:00', 
                                to = '2020-10-21T19:45Z', ), ), 
                        upload = vrt_lss_delivery.models.transport_load.TransportLoad(
                            count = 460, 
                            capacity = vrt_lss_delivery.models.capacity.Capacity(
                                mass = 10, 
                                volume = 2, 
                                capacity_x = 1, 
                                capacity_y = 2, 
                                capacity_z = 3, ), ), 
                        download = vrt_lss_delivery.models.transport_load.TransportLoad(
                            count = 460, 
                            capacity = vrt_lss_delivery.models.capacity.Capacity(
                                mass = 10, 
                                volume = 2, 
                                capacity_x = 1, 
                                capacity_y = 2, 
                                capacity_z = 3, ), ), 
                        current_load = vrt_lss_delivery.models.transport_load.TransportLoad(
                            count = 460, 
                            capacity = vrt_lss_delivery.models.capacity.Capacity(
                                mass = 10, 
                                volume = 2, 
                                capacity_x = 1, 
                                capacity_y = 2, 
                                capacity_z = 3, ), ), )
                    ],
        )

    def testTripStatistics(self):
        """Test TripStatistics"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
