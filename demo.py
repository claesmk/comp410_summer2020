import dfstools as dt
import featuretools as ft
import sys
import click
import os
import pandas as pd


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
    dt.load_csv_to_df('data', traverse_subdir=True)
    print('')

    print('traverse_subdir==False')
    dt.load_csv_to_df('data', traverse_subdir=False)

    return None


def demo_find_related_cols_by_content():
    # Important note - these hard-coded paths will work only on Linux or Mac
    # For a PC, path would be 'data\\airlines\\airlines.csv'
    dataframe_dict = {'airlines': pd.read_csv('data/airlines/airlines.csv'),
                      'flights': pd.read_csv('data/flights/flights.csv')}

    print(dt.find_related_cols_by_content(dataframe_dict))


# demonstration - this will be removed later
if __name__ == "__main__":
    print(sys.version)
    print(sys.executable)

    print('--- demo_load_csv_to_df() ---')
    demo_load_csv_to_df()
    print('---')

    print('--- demo_find_related_cols_by_content() ---')
    demo_find_related_cols_by_content()
    print('---')

    exit(1)

    relationship_dict = dt.get_dataset_dtypes(None)
    print(relationship_dict)

    relationship_dict = dt.find_primary_key_candidates(None, relationship_dict)
    print(relationship_dict)

    relationship_dict = dt.find_related_cols_by_name(None, relationship_dict)
    print(relationship_dict)

    relationship_dict = dt.find_parent_child_relationships(None, relationship_dict)
    print(relationship_dict)
