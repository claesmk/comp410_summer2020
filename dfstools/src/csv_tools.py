import pandas as pd
import os


# Prints aggie pride message
def show_aggie_pride():
    print('Aggie Pride - Worldwide')


def find_csv_files(path, include_hidden, traverse_subdir, follow_symlink):
    file_list = []

    if path is not None:
        if not traverse_subdir:
            for name in os.listdir(path):
                if name.endswith('.csv'):
                    file_list.append(os.path.join(path, name))
        else:
            for dirpath, dirnames, files in os.walk(path):
                for name in files:
                    if name.startswith('.'):
                        print(name + ' is hidden!')
                    elif name.endswith('.csv'):
                        file_list.append(os.path.join(dirpath, name))
    return file_list


def dataframes_from_file_list(file_list: list, ignore_errors: bool) -> dict:
    # Initialize the return structure
    dataframe_dict = {}

    # loop through each file (full path)
    #   one/two/three/four/file_name.csv
    for file in file_list:
        # display which file is being loaded
        print('Loading ' + file)

        # get the name of the file without the
        # .csv extension.  Use this as an index
        # in the return dict
        file_name = os.path.splitext(os.path.basename(file))[0]

        # attempt to read the dataframe
        try:
            dataframe_dict[file_name] = pd.read_csv(file)
        except (pd.errors.ParserError, pd.errors.EmptyDataError) as e:
            # if ignore_errors == True display a message
            # and continue processing
            if ignore_errors:
                print('Ignoring Error file not loaded: ' + file)
                print(e)
            # if ignore_errors == False throw an exception
            else:
                print('ParseError file not loaded: ' + file)
                raise e

    # return the dataframes
    return dataframe_dict


def load_csv_to_df(path, include_hidden=False, traverse_subdir=True, follow_symlink=False, ignore_errors=False):
    # path
    #    Starting path location to begin search
    #
    # include_hidden
    #     True  = Include any hidden files found while searching
    #     False = Ignore hidden files
    #
    # traverse_subdir
    #     True  = Traverse into any sub-directories found in <path>
    #     False = Do not traverse sub-directories
    #
    # follow_symlink
    #     True  = Follow any symbolic links
    #     False = Do not follow symbolic links
    #
    # ignore_errors
    #    False = Throw exception whenever an error is encountered
    #    True  = Print error message but continue processing

    file_list = find_csv_files(path, include_hidden, traverse_subdir, follow_symlink)
    return dataframes_from_file_list(file_list, ignore_errors)
