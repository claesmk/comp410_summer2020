import pandas as pd


def find_related_cols_by_name(dataframe_list, relationship_dict=None):
    # dataframe_list
    #     List of pandas dataframe objects
    if dataframe_list is None:
        return relationship_dict

    # relationship_dict
    #     This is an existing relationship_dict.  If None, a new
    #     relationship_dict should be created
    if relationship_dict is None:
        relationship_dict = {}

    for table in dataframe_list:
        # create a short-hand reference to the actual dataframe
        df = dataframe_list[table]

        # If this table is not in the relationship_dict, add it
        if table not in relationship_dict:
            relationship_dict[table] = {}

        # If a column is not in the relationship dict, add it
        for col in df.columns:
            if col not in relationship_dict[table]:
                relationship_dict[table][col] = {'relationships': []}

    # build the relationship table
    for table in dataframe_list:
        for col in dataframe_list[table].columns:
            # Want to compare all tables to every other table excep itself
            for related_table in relationship_dict:
                if related_table != table:
                    for related_col in relationship_dict[related_table]:
                        # If the names match
                        if col == related_col:
                            # TODO prints are for development only - remove later
                            print('found relationship')
                            print(table, end=': ')
                            print(col)
                            print(related_table, end=': ')
                            print(related_col)
                            new_relationship = {table+'.'+col: {}}
                            relationship_dict[related_table][related_col]['relationships'].append(new_relationship)

    # return relationship structure
    return relationship_dict


def find_similar_data(current_table, current_col, dataframe_dict):
    # Will return empty list if no relationships found
    relationship_list = []

    # create a target set which will be used for comparisons
    target_set = set(dataframe_dict[current_table][current_col])
    for table in dataframe_dict:
        if table != current_table:
            for col in dataframe_dict[table].columns:
                compare_set = set(dataframe_dict[table][col])
                if target_set.issubset(compare_set) or target_set.issubset(compare_set):
                    relationship_list.append({table + '.' + col: {}})

    return relationship_list


def find_related_cols_by_content(dataframe_list, relationship_dict=None):
    # dataframe_list
    #     List of pandas dataframe objects
    if dataframe_list is None:
        return relationship_dict

    # relationship_dict
    #     This is an existing relationship_dict.  If None, a new
    #     relationship_dict should be created
    if relationship_dict is None:
        relationship_dict = {}

    for table in dataframe_list:
        # create a short-hand reference to the actual dataframe
        df = dataframe_list[table]

        # If this table is not in the relationship_dict, add it
        if table not in relationship_dict:
            relationship_dict[table] = {}

        # If a column is not in the relationship dict, add it
        for col in df.columns:
            if col not in relationship_dict[table]:
                relationship_dict[table][col] = {}

            relationship_dict[table][col]['relationships'] = find_similar_data(table, col, dataframe_list)

    # return relationship structure
    return relationship_dict


def find_parent_child_relationships(dataframe_list, relationship_dict, hints=None):
    # dataframe_list
    #     List of pandas dataframe objects
    #
    # relationship_dict
    #     And existing relationship_dict is required
    #
    # hints
    #     Structure containing hints in cases where the data is ambiguous such
    #     as when two columns are related and appear to be primary key candidates
    #     in both tables. Format is:
    #         [{parent table.column: child table.column}, ...]

    ###
    # Student code (create additional functions as necessary)
    ###

    # mock-up for demonstration - remove after development
    relationship_dict['airlines']['carrier']['relationships'] = [{'flights.carrier': {'type': 'Parent'}}]
    relationship_dict['airports']['dest']['relationships'] = [{'flights.dest': {'type': 'Parent'}}]
    relationship_dict['flights']['dest']['relationships'] = [{'airports.dest': {'type': 'Child'}}]
    relationship_dict['flights']['carrier']['relationships'] = [{'airlines.carrier': {'type': 'Child'}}]
    relationship_dict['flights']['flight_id']['relationships'] = [{'trip_logs.flight_id': {'type': 'Parent'}}]
    relationship_dict['trip_logs']['flight_id']['relationships'] = [{'flights.flight_id': {'type': 'Child'}}]

    # return relationship structure
    return relationship_dict
