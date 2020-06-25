import unittest
import pytest
import git
import os
import pandas as pd
from dfstools import show_aggie_pride
from dfstools import load_csv_to_df


class CsvTools(unittest.TestCase):
    @pytest.fixture(autouse=True)
    def _pass_fixtures(self, capsys):
        self.capsys = capsys

    def test_show_aggie_pride(self):
        show_aggie_pride()

        # read the capture buffer so far
        out, err = self.capsys.readouterr()

        # make sure the message was actually printed 
        self.assertEqual('Aggie Pride - Worldwide\n', out)

    def test_load_csv_to_df(self):
        expected = ['airlines', 'airports', 'flights', 'trip_logs']

        # Try to load files from data directory in the path to the current repo
        data_path = os.path.join(git.Repo('.', search_parent_directories=True).working_tree_dir, 'data')

        # Test don't traverse into sub directories
        result = load_csv_to_df(data_path, traverse_subdir=False)
        self.assertEqual(result, {})

        result = load_csv_to_df(data_path, ignore_errors=True)

        # Check to make sure each expected table was loaded
        for table in expected:
            self.assertIn(table, result.keys())

    def test_load_csv_to_df_ignore_errors(self):
        expected = ['airlines', 'airports', 'flights', 'trip_logs']

        # Try to load files from data directory in the path to the current repo
        data_path = os.path.join(git.Repo('.', search_parent_directories=True).working_tree_dir, 'data')

        # Make sure the correct exceptions are generated
        with self.assertRaises((pd.errors.ParserError, pd.errors.EmptyDataError)) as e_info:
            load_csv_to_df(data_path, ignore_errors=False)


if __name__ == '__main__':
    unittest.main()
