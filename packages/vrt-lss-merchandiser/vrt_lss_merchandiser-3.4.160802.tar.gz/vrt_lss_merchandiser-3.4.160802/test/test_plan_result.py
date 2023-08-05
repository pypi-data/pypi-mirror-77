# coding: utf-8

"""
    VeeRoute.LSS Merchandiser

    VeeRoute.LSS Merchandiser API  # noqa: E501

    The version of the OpenAPI document: 3.4.160802
    Contact: support@veeroute.com
    Generated by: https://openapi-generator.tech
"""


from __future__ import absolute_import

import unittest
import datetime

import vrt_lss_merchandiser
from vrt_lss_merchandiser.models.plan_result import PlanResult  # noqa: E501
from vrt_lss_merchandiser.rest import ApiException

class TestPlanResult(unittest.TestCase):
    """PlanResult unit test stubs"""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def make_instance(self, include_optional):
        """Test PlanResult
            include_option is a boolean, when False only required
            params are included, when True both required and
            optional params are included """
        # model = vrt_lss_merchandiser.models.plan_result.PlanResult()  # noqa: E501
        if include_optional :
            return PlanResult(
                tracedata = vrt_lss_merchandiser.models.trace_data.TraceData(
                    code = 'client_server_service_time_id', ), 
                timetable = vrt_lss_merchandiser.models.performer.Performer(
                    key = 'performer0001', 
                    start_location = vrt_lss_merchandiser.models.location.Location(
                        latitude = 55.692789, 
                        longitude = 37.554554, 
                        arrival_duration = 15, 
                        departure_duration = 5, ), 
                    finish_location = vrt_lss_merchandiser.models.location.Location(
                        latitude = 55.692789, 
                        longitude = 37.554554, 
                        arrival_duration = 15, 
                        departure_duration = 5, ), 
                    transport_type = 'CAR', 
                    shifts = [
                        vrt_lss_merchandiser.models.shift.Shift(
                            availability_time = vrt_lss_merchandiser.models.time_window.TimeWindow(
                                from = '2020-10-21T09:30+03:00', 
                                to = '2020-10-21T19:45Z', ), 
                            working_time = vrt_lss_merchandiser.models.time_window.TimeWindow(
                                from = '2020-10-21T09:30+03:00', 
                                to = '2020-10-21T19:45Z', ), 
                            trip = vrt_lss_merchandiser.models.trip.Trip(
                                key = 'trip01', 
                                trip_time = vrt_lss_merchandiser.models.time_window.TimeWindow(
                                    from = '2020-10-21T09:30+03:00', 
                                    to = '2020-10-21T19:45Z', ), 
                                actions = [
                                    vrt_lss_merchandiser.models.order_action.OrderAction(
                                        order = vrt_lss_merchandiser.models.order.Order(
                                            key = 'order0001', 
                                            location = vrt_lss_merchandiser.models.location.Location(
                                                latitude = 55.692789, 
                                                longitude = 37.554554, 
                                                arrival_duration = 15, 
                                                departure_duration = 5, ), 
                                            visits = [
                                                vrt_lss_merchandiser.models.event_window.EventWindow(
                                                    time_window = vrt_lss_merchandiser.models.time_window.TimeWindow(
                                                        from = '2020-10-21T09:30+03:00', 
                                                        to = '2020-10-21T19:45Z', ), )
                                                ], 
                                            facts = [
                                                vrt_lss_merchandiser.models.event_window.EventWindow(
                                                    time_window = vrt_lss_merchandiser.models.time_window.TimeWindow(
                                                        from = '2020-10-21T09:30+03:00', 
                                                        to = '2020-10-21T19:45Z', ), )
                                                ], 
                                            duration = 30, 
                                            reward = 199.1, ), 
                                        order_time = vrt_lss_merchandiser.models.time_window.TimeWindow(
                                            from = '2020-10-21T09:30+03:00', 
                                            to = '2020-10-21T19:45Z', ), 
                                        location_time = vrt_lss_merchandiser.models.time_window.TimeWindow(
                                            from = '2020-10-21T09:30+03:00', 
                                            to = '2020-10-21T19:45Z', ), )
                                    ], 
                                waitlist = [
                                    vrt_lss_merchandiser.models.trip_waitlist.Trip_waitlist()
                                    ], ), )
                        ], 
                    tariff = vrt_lss_merchandiser.models.tariff.Tariff(
                        basic = vrt_lss_merchandiser.models.tariff_primary.TariffPrimary(
                            cost_per_shift = 1000, 
                            cost_per_meter = 0.1, 
                            max_length = 200000, 
                            cost_per_minute = 0.2, 
                            max_time = 480, ), 
                        extra = [
                            vrt_lss_merchandiser.models.tariff_primary.TariffPrimary(
                                cost_per_shift = 1000, 
                                cost_per_meter = 0.1, 
                                max_length = 200000, 
                                cost_per_minute = 0.2, 
                                max_time = 480, )
                            ], ), ), 
                statistics = vrt_lss_merchandiser.models.plan_statistics.PlanStatistics(
                    total_statistics = vrt_lss_merchandiser.models.statistics.Statistics(
                        cost = 1231.1, 
                        reward = 2343.3, 
                        measurements = vrt_lss_merchandiser.models.measurements.Measurements(
                            driving_time = 15, 
                            waiting_time = 5, 
                            working_time = 50, 
                            arriving_time = 30, 
                            departure_time = 20, 
                            total_time = 120, 
                            distance = 5200, 
                            time_window = vrt_lss_merchandiser.models.time_window.TimeWindow(
                                from = '2020-10-21T09:30+03:00', 
                                to = '2020-10-21T19:45Z', ), ), 
                        orders_count = 1700, 
                        performers_count = 257, 
                        capacity_utilization = vrt_lss_merchandiser.models.capacity.Capacity(
                            mass = 10, 
                            volume = 2, 
                            capacity_x = 1, 
                            capacity_y = 2, 
                            capacity_z = 3, ), 
                        capacity_max = vrt_lss_merchandiser.models.capacity.Capacity(
                            mass = 10, 
                            volume = 2, 
                            capacity_x = 1, 
                            capacity_y = 2, 
                            capacity_z = 3, ), ), 
                    trips_statistics = [
                        vrt_lss_merchandiser.models.trip_statistics.TripStatistics(
                            trip_key = 'trip01', 
                            statistics = vrt_lss_merchandiser.models.statistics.Statistics(
                                cost = 1231.1, 
                                reward = 2343.3, 
                                measurements = vrt_lss_merchandiser.models.measurements.Measurements(
                                    driving_time = 15, 
                                    waiting_time = 5, 
                                    working_time = 50, 
                                    arriving_time = 30, 
                                    departure_time = 20, 
                                    total_time = 120, 
                                    distance = 5200, ), 
                                orders_count = 1700, 
                                performers_count = 257, ), 
                            stop_statistics = [
                                vrt_lss_merchandiser.models.stop_statistics.StopStatistics(
                                    location = vrt_lss_merchandiser.models.location.Location(
                                        latitude = 55.692789, 
                                        longitude = 37.554554, 
                                        arrival_duration = 15, 
                                        departure_duration = 5, ), 
                                    location_key = 'location01', 
                                    demand_ids = [
                                        'demand01'
                                        ], 
                                    measurements = vrt_lss_merchandiser.models.measurements.Measurements(
                                        driving_time = 15, 
                                        waiting_time = 5, 
                                        working_time = 50, 
                                        arriving_time = 30, 
                                        departure_time = 20, 
                                        total_time = 120, 
                                        distance = 5200, ), 
                                    upload = vrt_lss_merchandiser.models.transport_load.TransportLoad(
                                        count = 460, 
                                        capacity = vrt_lss_merchandiser.models.capacity.Capacity(
                                            mass = 10, 
                                            volume = 2, 
                                            capacity_x = 1, 
                                            capacity_y = 2, 
                                            capacity_z = 3, ), ), 
                                    download = vrt_lss_merchandiser.models.transport_load.TransportLoad(
                                        count = 460, 
                                        capacity = vrt_lss_merchandiser.models.capacity.Capacity(
                                            mass = 10, 
                                            volume = 2, 
                                            capacity_x = 1, 
                                            capacity_y = 2, 
                                            capacity_z = 3, ), ), 
                                    current_load = vrt_lss_merchandiser.models.transport_load.TransportLoad(
                                        count = 460, 
                                        capacity = vrt_lss_merchandiser.models.capacity.Capacity(
                                            mass = 10, 
                                            volume = 2, 
                                            capacity_x = 1, 
                                            capacity_y = 2, 
                                            capacity_z = 3, ), ), )
                                ], 
                            total_load = vrt_lss_merchandiser.models.transport_load.TransportLoad(
                                count = 460, 
                                capacity = vrt_lss_merchandiser.models.capacity.Capacity(
                                    mass = 10, 
                                    volume = 2, 
                                    capacity_x = 1, 
                                    capacity_y = 2, 
                                    capacity_z = 3, ), ), 
                            max_load = vrt_lss_merchandiser.models.transport_load.TransportLoad(
                                count = 460, 
                                capacity = vrt_lss_merchandiser.models.capacity.Capacity(
                                    mass = 10, 
                                    volume = 2, 
                                    capacity_x = 1, 
                                    capacity_y = 2, 
                                    capacity_z = 3, ), ), )
                        ], ), 
                validations = [
                    vrt_lss_merchandiser.models.validation.Validation(
                        type = 'info', 
                        entity_key = 'ord0001', 
                        entity_type = 'order', 
                        info = 'bad time windows', )
                    ], 
                unplanned_orders = [
                    vrt_lss_merchandiser.models.unplanned_order.UnplannedOrder(
                        order = vrt_lss_merchandiser.models.order.Order(
                            key = 'order0001', 
                            location = vrt_lss_merchandiser.models.location.Location(
                                latitude = 55.692789, 
                                longitude = 37.554554, 
                                arrival_duration = 15, 
                                departure_duration = 5, ), 
                            visits = [
                                vrt_lss_merchandiser.models.event_window.EventWindow(
                                    time_window = vrt_lss_merchandiser.models.time_window.TimeWindow(
                                        from = '2020-10-21T09:30+03:00', 
                                        to = '2020-10-21T19:45Z', ), )
                                ], 
                            facts = [
                                vrt_lss_merchandiser.models.event_window.EventWindow(
                                    time_window = vrt_lss_merchandiser.models.time_window.TimeWindow(
                                        from = '2020-10-21T09:30+03:00', 
                                        to = '2020-10-21T19:45Z', ), )
                                ], 
                            duration = 30, 
                            reward = 199.1, ), 
                        reason = 'undefined', )
                    ], 
                progress = 50, 
                info = vrt_lss_merchandiser.models.plan_info.PlanInfo(
                    status = 'FINISHED_IN_TIME', 
                    result_version = 13, 
                    planning_time = 10, 
                    waiting_time = 5, )
            )
        else :
            return PlanResult(
        )

    def testPlanResult(self):
        """Test PlanResult"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
