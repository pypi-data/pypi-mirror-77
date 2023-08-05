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
from vrt_lss_lastmile.models.plan_result import PlanResult  # noqa: E501
from vrt_lss_lastmile.rest import ApiException

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
        # model = vrt_lss_lastmile.models.plan_result.PlanResult()  # noqa: E501
        if include_optional :
            return PlanResult(
                tracedata = vrt_lss_lastmile.models.trace_data.TraceData(
                    code = 'client_server_service_time_id', ), 
                trips = [
                    vrt_lss_lastmile.models.trip.Trip(
                        key = 'TRIP0001', 
                        assigned_shifts = [
                            vrt_lss_lastmile.models.assigned_shift.AssignedShift(
                                shift_key = 'performer01', 
                                shift_time = vrt_lss_lastmile.models.time_window.TimeWindow(
                                    from = '2020-10-21T09:30+03:00', 
                                    to = '2020-10-21T19:45Z', ), )
                            ], 
                        actions = [
                            vrt_lss_lastmile.models.trip_action.TripAction(
                                order_key = 'order01', 
                                demand_key = 'demand01.1', 
                                location_key = 'location01', 
                                todolist = [
                                    vrt_lss_lastmile.models.trip_job.TripJob(
                                        job_type = 'START_WORK', 
                                        job_time = '2020-10-21T09:30+03:00', )
                                    ], 
                                cargo_placements = [
                                    vrt_lss_lastmile.models.cargo_placement.CargoPlacement(
                                        box_key = 'box01', 
                                        cargo_key = 'cargo01', )
                                    ], )
                            ], 
                        waitlist = ["order02"], )
                    ], 
                statistics = vrt_lss_lastmile.models.plan_statistics.PlanStatistics(
                    total_statistics = vrt_lss_lastmile.models.statistics.Statistics(
                        cost = 1231.1, 
                        reward = 2343.3, 
                        measurements = vrt_lss_lastmile.models.measurements.Measurements(
                            driving_time = 15, 
                            waiting_time = 5, 
                            working_time = 50, 
                            arriving_time = 30, 
                            departure_time = 20, 
                            total_time = 120, 
                            distance = 5200, 
                            time_window = vrt_lss_lastmile.models.time_window.TimeWindow(
                                from = '2020-10-21T09:30+03:00', 
                                to = '2020-10-21T19:45Z', ), ), 
                        orders_count = 1700, 
                        performers_count = 257, 
                        capacity_utilization = vrt_lss_lastmile.models.capacity.Capacity(
                            mass = 10, 
                            volume = 2, 
                            capacity_x = 1, 
                            capacity_y = 2, 
                            capacity_z = 3, ), 
                        capacity_max = vrt_lss_lastmile.models.capacity.Capacity(
                            mass = 10, 
                            volume = 2, 
                            capacity_x = 1, 
                            capacity_y = 2, 
                            capacity_z = 3, ), ), 
                    trips_statistics = [
                        vrt_lss_lastmile.models.trip_statistics.TripStatistics(
                            trip_key = 'trip01', 
                            statistics = vrt_lss_lastmile.models.statistics.Statistics(
                                cost = 1231.1, 
                                reward = 2343.3, 
                                measurements = vrt_lss_lastmile.models.measurements.Measurements(
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
                                vrt_lss_lastmile.models.stop_statistics.StopStatistics(
                                    location = vrt_lss_lastmile.models.location.Location(
                                        latitude = 55.692789, 
                                        longitude = 37.554554, 
                                        arrival_duration = 15, 
                                        departure_duration = 5, ), 
                                    location_key = 'location01', 
                                    demand_ids = [
                                        'demand01'
                                        ], 
                                    measurements = vrt_lss_lastmile.models.measurements.Measurements(
                                        driving_time = 15, 
                                        waiting_time = 5, 
                                        working_time = 50, 
                                        arriving_time = 30, 
                                        departure_time = 20, 
                                        total_time = 120, 
                                        distance = 5200, ), 
                                    upload = vrt_lss_lastmile.models.transport_load.TransportLoad(
                                        count = 460, 
                                        capacity = vrt_lss_lastmile.models.capacity.Capacity(
                                            mass = 10, 
                                            volume = 2, 
                                            capacity_x = 1, 
                                            capacity_y = 2, 
                                            capacity_z = 3, ), ), 
                                    download = vrt_lss_lastmile.models.transport_load.TransportLoad(
                                        count = 460, 
                                        capacity = vrt_lss_lastmile.models.capacity.Capacity(
                                            mass = 10, 
                                            volume = 2, 
                                            capacity_x = 1, 
                                            capacity_y = 2, 
                                            capacity_z = 3, ), ), 
                                    current_load = vrt_lss_lastmile.models.transport_load.TransportLoad(
                                        count = 460, 
                                        capacity = vrt_lss_lastmile.models.capacity.Capacity(
                                            mass = 10, 
                                            volume = 2, 
                                            capacity_x = 1, 
                                            capacity_y = 2, 
                                            capacity_z = 3, ), ), )
                                ], 
                            total_load = vrt_lss_lastmile.models.transport_load.TransportLoad(
                                count = 460, 
                                capacity = vrt_lss_lastmile.models.capacity.Capacity(
                                    mass = 10, 
                                    volume = 2, 
                                    capacity_x = 1, 
                                    capacity_y = 2, 
                                    capacity_z = 3, ), ), 
                            max_load = vrt_lss_lastmile.models.transport_load.TransportLoad(
                                count = 460, 
                                capacity = vrt_lss_lastmile.models.capacity.Capacity(
                                    mass = 10, 
                                    volume = 2, 
                                    capacity_x = 1, 
                                    capacity_y = 2, 
                                    capacity_z = 3, ), ), )
                        ], ), 
                validations = [
                    vrt_lss_lastmile.models.validation.Validation(
                        type = 'info', 
                        entity_key = 'ord0001', 
                        entity_type = 'order', 
                        info = 'bad time windows', )
                    ], 
                unplanned_orders = [
                    vrt_lss_lastmile.models.unplanned_order.UnplannedOrder(
                        order = vrt_lss_lastmile.models.order.Order(
                            key = 'order01', 
                            order_features = ["Special"], 
                            order_restrictions = ["Special"], 
                            performer_restrictions = ["B1"], 
                            performer_blacklist = ["B1"], 
                            cargos = [
                                vrt_lss_lastmile.models.cargo.Cargo(
                                    key = 'cargo01', 
                                    capacity = vrt_lss_lastmile.models.capacity.Capacity(
                                        mass = 10, 
                                        volume = 2, 
                                        capacity_x = 1, 
                                        capacity_y = 2, 
                                        capacity_z = 3, ), 
                                    width = 1, 
                                    height = 0.3, 
                                    length = 2.2, 
                                    max_storage_time = 60, 
                                    restrictions = ["Freezer"], )
                                ], 
                            demands = [
                                vrt_lss_lastmile.models.demand.Demand(
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
                                        ], )
                                ], ), 
                        reason = 'undefined', )
                    ], 
                progress = 50, 
                info = vrt_lss_lastmile.models.plan_info.PlanInfo(
                    status = 'FINISHED_IN_TIME', 
                    result_version = 13, 
                    planning_time = 10, 
                    waiting_time = 5, )
            )
        else :
            return PlanResult(
                trips = [
                    vrt_lss_lastmile.models.trip.Trip(
                        key = 'TRIP0001', 
                        assigned_shifts = [
                            vrt_lss_lastmile.models.assigned_shift.AssignedShift(
                                shift_key = 'performer01', 
                                shift_time = vrt_lss_lastmile.models.time_window.TimeWindow(
                                    from = '2020-10-21T09:30+03:00', 
                                    to = '2020-10-21T19:45Z', ), )
                            ], 
                        actions = [
                            vrt_lss_lastmile.models.trip_action.TripAction(
                                order_key = 'order01', 
                                demand_key = 'demand01.1', 
                                location_key = 'location01', 
                                todolist = [
                                    vrt_lss_lastmile.models.trip_job.TripJob(
                                        job_type = 'START_WORK', 
                                        job_time = '2020-10-21T09:30+03:00', )
                                    ], 
                                cargo_placements = [
                                    vrt_lss_lastmile.models.cargo_placement.CargoPlacement(
                                        box_key = 'box01', 
                                        cargo_key = 'cargo01', )
                                    ], )
                            ], 
                        waitlist = ["order02"], )
                    ],
        )

    def testPlanResult(self):
        """Test PlanResult"""
        inst_req_only = self.make_instance(include_optional=False)
        inst_req_and_optional = self.make_instance(include_optional=True)


if __name__ == '__main__':
    unittest.main()
