import dfstools as dt
import featuretools as ft
import sys
import click
import os
import pandas as pd
import pprint

pp = pprint.PrettyPrinter(width=41, compact=True)


def save_demo_data(es, file_list):
    for f in file_list:
        file_with_path = os.path.join('data', os.path.join(f, f + '.csv'))
        print(f'Saving {f} to {file_with_path}')
        es[f].df.to_csv(file_with_path, index=False)


def download_data():
    # check to see if data is already downloaded
    file_list = ['trip_logs', 'flights', 'airlines', 'airports']

    # If any file in the list is missing, download and save them all
    for f in file_list:
        file_with_path = os.path.join('data', os.path.join(f, f+'.csv'))
        if not os.path.exists(file_with_path):
            if click.confirm('OK to download demo featuretools data?', default=False):
                es = ft.demo.load_flight(verbose=True)
                save_demo_data(es, file_list)
                break


def demo_load_csv_to_df():
    print('traverse_subdir==True')
    print(dt.load_csv_to_df('data', traverse_subdir=True, ignore_errors=True))
    print('')

    print('traverse_subdir==False')
    print(dt.load_csv_to_df('data', traverse_subdir=False, ignore_errors=True))

    return None


def demo_find_related_cols_by_name():
    # Important note - these hard-coded paths will work only on Linux or Mac
    # For a PC, path would be 'data\\airlines\\airlines.csv'
    dataframe_dict = {'airlines': pd.read_csv('data/airlines/airlines.csv'),
                      'flights': pd.read_csv('data/flights/flights.csv'),
                      'airports': pd.read_csv('data/airports/airports.csv'),
                      'trip_logs': pd.read_csv('data/trip_logs/trip_logs.csv')}

    pp.pprint(dt.find_related_cols_by_name(dataframe_dict))


def demo_find_related_cols_by_content():
    # Important note - these hard-coded paths will work only on Linux or Mac
    # For a PC, path would be 'data\\airlines\\airlines.csv'
    dataframe_dict = {'airlines': pd.read_csv('data/airlines/airlines.csv'),
                      'flights': pd.read_csv('data/flights/flights.csv')}

    pp.pprint(dt.find_related_cols_by_content(dataframe_dict))


def demo_find_parent_child_relationships():
    # Create a mock-up dataframe list
    dataframe_list = ['airlines', 'airports', 'flights', 'trip_logs']

    # Get the data types of each object in each dataframe
    relationship_dict = dt.get_dataset_dtypes(dataframe_list)

    # Identify primary key candidates
    relationship_dict = dt.find_primary_key_candidates(dataframe_list, relationship_dict)

    # Identify relationships by column name
    relationship_dict = dt.find_related_cols_by_name(dataframe_list, relationship_dict)

    relationship_dict = dt.find_parent_child_relationships(dataframe_list, relationship_dict)
    pp.pprint(relationship_dict)

    # dataframe_dict = dt.load_csv_to_df('data', ignore_errors=True)
    #
    # relationship_dict = dt.find_related_cols_by_name(dataframe_dict, None)
    #
    # relationship_dict = dt.find_parent_child_relationships(dataframe_dict, relationship_dict)
    # pp.pprint(relationship_dict)


# import pandas as pd
def demo_pandas():
    # Important note - these hard-coded paths will work only on Linux or Mac
    # For a PC, path would be 'data\\airlines\\airlines.csv'
    # This is the format that
    dataframe_dict = {'airlines': pd.read_csv('data/airlines/airlines.csv'),
                      'flights': pd.read_csv('data/flights/flights.csv'),
                      'airports': pd.read_csv('data/airports/airports.csv')}

    # Initialize relationships
    relationships_dict = {}

    for table in dataframe_dict:
        # Initialize relationships for this table
        relationships_dict[table] = {}

        print('table name', end=': ')
        print(table)
        print('columns')
        print(dataframe_dict[table].columns)

        for col in dataframe_dict[table].columns:
            dtype_str = str(dataframe_dict[table][col].dtype)
            relationships_dict[table][col] = {'dtype': dtype_str}

    print('relationships')
    print(relationships_dict)


def run_demo():
    print(sys.version)
    print(sys.executable)

    print('--- demo_load_csv_to_df() ---')
    demo_load_csv_to_df()
    print('---')

    print('--- demo_find_related_cols_by_name() ---')
    demo_find_related_cols_by_name()
    print('---')

    print('--- demo_find_related_cols_by_content() ---')
    demo_find_related_cols_by_content()
    print('---')

    print('--- demo_find_parent_child_relationships ---')
    demo_find_parent_child_relationships()
    print('---')

    print('--- demo pandas ---')
    demo_pandas()
    print('---')

    # print('other demo functions')
    #
    # relationship_dict = dt.get_dataset_dtypes(None)
    # print(relationship_dict)
    #
    # relationship_dict = dt.find_primary_key_candidates(None, relationship_dict)
    # print(relationship_dict)
    #
    # relationship_dict = dt.find_parent_child_relationships(None, relationship_dict)
    # print(relationship_dict)


# demonstration - this will be removed later
if __name__ == "__main__":
    run_demo()
