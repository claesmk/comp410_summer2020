import unittest
import pandas as pd
import os
import git
from dfstools import load_csv_to_df
from dfstools import get_dataset_dtypes
from dfstools import find_primary_key_candidates
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
                                'origin': {'relationships': [{'airports.dest': {}}]},
                                'origin_city': {'relationships': [{'airports.dest_city': {}}]},
                                'origin_state': {'relationships': [{'airports.dest_state': {}}]}},
                    'trip_logs': {'air_time': {'relationships': []},
                                  'arr_delay': {'relationships': [{'flights.distance_group': {}}]},
                                  'arr_time': {'relationships': []},
                                  'canceled': {'relationships': []},
                                  'carrier_delay': {'relationships': [{'flights.distance_group': {}}]},
                                  'date_scheduled': {'relationships': []},
                                  'dep_delay': {'relationships': [{'flights.distance_group': {}}]},
                                  'dep_time': {'relationships': []},
                                  'distance': {'relationships': []},
                                  'diverted': {'relationships': []},
                                  'flight_id': {'relationships': [{'flights.flight_id': {}}]},
                                  'late_aircraft_delay': {'relationships': [{'flights.distance_group': {}}]},
                                  'national_airspace_delay': {'relationships': [{'flights.distance_group': {}}]},
                                  'scheduled_arr_time': {'relationships': []},
                                  'scheduled_dep_time': {'relationships': []},
                                  'scheduled_elapsed_time': {'relationships': []},
                                  'security_delay': {'relationships': [{'flights.distance_group': {}}]},
                                  'taxi_in': {'relationships': [{'flights.distance_group': {}}]},
                                  'taxi_out': {'relationships': [{'flights.distance_group': {}}]},
                                  'trip_log_id': {'relationships': [{'flights.distance_group': {}},
                                                                    {'flights.flight_num': {}}]},
                                  'weather_delay': {'relationships': [{'flights.distance_group': {}}]}}}

        result = find_related_cols_by_content(dataframe_dict, None)
        self.assertEqual(result, expected)

    def test_find_parent_child_relationships(self):
        dataframe_list = ['airlines', 'airports', 'flights', 'trip_logs']

        expected = {'airlines': {'carrier': {'dtype': 'O',
                                             'key_candidate': True,
                                             'relationships': [{'flights.carrier': {'type': 'Parent'}}]}},
                    'airports': {'dest': {'dtype': 'O',
                                          'key_candidate': True,
                                          'relationships': [{'flights.dest': {'type': 'Parent'}}]}},
                    'flights': {'carrier': {'dtype': 'O',
                                            'key_candidate': False,
                                            'relationships': [{'airlines.carrier': {'type': 'Child'}}]},
                                'dest': {'dtype': 'O',
                                         'key_candidate': False,
                                         'relationships': [{'airports.dest': {'type': 'Child'}}]},
                                'flight_id': {'dtype': 'O',
                                              'key_candidate': True,
                                              'relationships': [{'trip_logs.flight_id': {'type': 'Parent'}}]}},
                    'trip_logs': {'flight_id': {'dtype': 'O',
                                                'key_candidate': False,
                                                'relationships': [{'flights.flight_id': {'type': 'Child'}}]}}}

        # Get the data types of each object in each dataframe
        relationship_dict = get_dataset_dtypes(dataframe_list)

        # Identify primary key candidates
        relationship_dict = find_primary_key_candidates(dataframe_list, relationship_dict)

        # Identify relationships by column name
        relationship_dict = find_related_cols_by_name(dataframe_list, relationship_dict)

        relationship_dict = find_parent_child_relationships(dataframe_list, relationship_dict)
        self.assertEqual(relationship_dict, expected)


if __name__ == '__main__':
    unittest.main()
