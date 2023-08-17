""" 
Some usefull methods on dataframes to save some lines and reduce code error.
""" 

# IMPORTS
import pandas as pd
import time
import os

def join_dataframe(dataframes):
    """
    This method joins in columns several csv's.
    """
    if dataframes == None:
        print("Write the file names")
        return
    df = pd.read_csv(dataframes[0])
    for dataframe in dataframes[1:]:
        df2 = pd.read_csv(dataframe)
        df = pd.merge(df, df2, on=["query"], how='outer')
        #df = pd.concat([df, df2], axis=1)

    time_STAMP = time.strftime("%Y%m%d%H%M%S")
    df.to_csv("{}join_dataframe.csv".format(time_STAMP), index=False)


def sort_dataframe(csvs, column, asc):
    """
    Sort one or more csv's by a column in descending or ascending order
    
    Arguments:
        csvs {list} -- list of csv files
        column {string} -- column
        desc {int} -- 1 if asc and 0 if desc
    """
    
    for csv in csvs:
        print(csv)
        directorio = os.path.dirname(csv)
        name = os.path.splitext(os.path.basename(csv))[0]
        df = pd.read_csv(csv)
        if asc == 1:
            df = df.sort_values(by=column, ascending=True)
        else:
            df = df.sort_values(by=column, ascending=False)
        df.to_csv("{}/sortby_{}_{}.csv".format(directorio, column, name), index=False)
