import unittest
import pandas as pd
import os
import git
from dfstools import load_csv_to_df
from dfstools import find_related_cols_by_name
from dfstools import find_related_cols_by_content
from dfstools import find_parent_child_relationships


class DataTools(unittest.TestCase):
    def test_find_related_cols_by_name(self):
        # load the test data
        data_path = os.path.join(git.Repo('.', search_parent_directories=True).working_tree_dir, 'data')
        dataframe_dict = load_csv_to_df(data_path, ignore_errors=True)

        expected = {'airlines': {'carrier': {'relationships': [{'flights.carrier': {}}]}},
                    'airports': {'dest': {'relationships': [{'flights.dest': {}}]},
                                 'dest_city': {'relationships': []},
                                 'dest_state': {'relationships': []}},
                    'flights': {'carrier': {'relationships': [{'airlines.carrier': {}}]},
                                'dest': {'relationships': [{'airports.dest': {}}]},
                                'distance_group': {'relationships': []},
                                'first_trip_logs_time': {'relationships': []},
                                'flight_id': {'relationships': [{'trip_logs.flight_id': {}}]},
                                'flight_num': {'relationships': []},
                                'origin': {'relationships': []},
                                'origin_city': {'relationships': []},
                                'origin_state': {'relationships': []}},
                    'trip_logs': {'air_time': {'relationships': []},
                                  'arr_delay': {'relationships': []},
                                  'arr_time': {'relationships': []},
                                  'canceled': {'relationships': []},
                                  'carrier_delay': {'relationships': []},
                                  'date_scheduled': {'relationships': []},
                                  'dep_delay': {'relationships': []},
                                  'dep_time': {'relationships': []},
                                  'distance': {'relationships': []},
                                  'diverted': {'relationships': []},
                                  'flight_id': {'relationships': [{'flights.flight_id': {}}]},
                                  'late_aircraft_delay': {'relationships': []},
                                  'national_airspace_delay': {'relationships': []},
                                  'scheduled_arr_time': {'relationships': []},
                                  'scheduled_dep_time': {'relationships': []},
                                  'scheduled_elapsed_time': {'relationships': []},
                                  'security_delay': {'relationships': []},
                                  'taxi_in': {'relationships': []},
                                  'taxi_out': {'relationships': []},
                                  'trip_log_id': {'relationships': []},
                                  'weather_delay': {'relationships': []}}}

        result = find_related_cols_by_name(dataframe_dict, None)
        self.assertEqual(result, expected)

    def test_find_related_cols_by_content(self):
        # load the test data
        data_path = os.path.join(git.Repo('.', search_parent_directories=True).working_tree_dir, 'data')
        dataframe_dict = load_csv_to_df(data_path, ignore_errors=True)

        expected = {'airlines': {'carrier': {'relationships': [{'flights.carrier': {}}]}},
                    'airports': {'dest': {'relationships': [{'flights.origin': {}},
                                                            {'flights.dest': {}}]},
                                 'dest_city': {'relationships': [{'flights.origin_city': {}}]},
                                 'dest_state': {'relationships': [{'flights.origin_state': {}}]}},
                    'flights': {'carrier': {'relationships': [{'airlines.carrier': {}}]},
                                'dest': {'relationships': [{'airports.dest': {}}]},
                                'distance_group': {'relationships': [{'trip_logs.trip_log_id': {}},
                                                                     {'trip_logs.dep_delay': {}},
                                                                     {'trip_logs.taxi_out': {}},
                                                                     {'trip_logs.taxi_in': {}},
                                                                     {'trip_logs.arr_delay': {}},
                                                                     {'trip_logs.carrier_delay': {}},
                                                                     {'trip_logs.weather_delay': {}},
                                                                     {'trip_logs.national_airspace_delay': {}},
                                                                     {'trip_logs.security_delay': {}},
                                                                     {'trip_logs.late_aircraft_delay': {}}]},
                                'first_trip_logs_time': {'relationships': []},
                                'flight_id': {'relationships': [{'trip_logs.flight_id': {}}]},
                                'flight_num': {'relationships': [{'trip_logs.trip_log_id': {}}]},
                                'origin': {'relationships': []},
                                'origin_city': {'relationships': []},
                                'origin_state': {'relationships': [{'airports.dest_state': {}}]}},
                    'trip_logs': {'air_time': {'relationships': []},
                                  'arr_delay': {'relationships': []},
                                  'arr_time': {'relationships': []},
                                  'canceled': {'relationships': []},
                                  'carrier_delay': {'relationships': []},
                                  'date_scheduled': {'relationships': []},
                                  'dep_delay': {'relationships': []},
                                  'dep_time': {'relationships': []},
                                  'distance': {'relationships': []},
                                  'diverted': {'relationships': []},
                                  'flight_id': {'relationships': [{'flights.flight_id': {}}]},
                                  'late_aircraft_delay': {'relationships': []},
                                  'national_airspace_delay': {'relationships': []},
                                  'scheduled_arr_time': {'relationships': []},
                                  'scheduled_dep_time': {'relationships': []},
                                  'scheduled_elapsed_time': {'relationships': []},
                                  'security_delay': {'relationships': []},
                                  'taxi_in': {'relationships': []},
                                  'taxi_out': {'relationships': []},
                                  'trip_log_id': {'relationships': []},
                                  'weather_delay': {'relationships': []}}}

        result = find_related_cols_by_content(dataframe_dict, None)
        self.assertEqual(result, expected)

    def test_find_parent_child_relationships(self):
        expected = {'airlines': {'carrier': {'relationships': [{'flights.carrier': {}}]}},
                    'airports': {'dest': {'relationships': [{'flights.dest': {}}]},
                                 'dest_city': {'relationships': []},
                                 'dest_state': {'relationships': []}},
                    'flights': {'carrier': {'relationships': [{'airlines.carrier': {}}]},
                                'dest': {'relationships': [{'airports.dest': {}}]},
                                'distance_group': {'relationships': []},
                                'first_trip_logs_time': {'relationships': []},
                                'flight_id': {'relationships': [{'trip_logs.flight_id': {}}]},
                                'flight_num': {'relationships': []},
                                'origin': {'relationships': []},
                                'origin_city': {'relationships': []},
                                'origin_state': {'relationships': []}},
                    'trip_logs': {'flight_id': {'relationships': []}}}

        result = find_parent_child_relationships(None, expected)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
