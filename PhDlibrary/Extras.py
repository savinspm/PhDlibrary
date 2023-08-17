
import time
import os

def times():
    ''' time_high_resolution_counter.py
    measure elapsed time of a Python calculation
    time.perf_counter() is new in Python 3.3
    '''

    # returned value is in fractional seconds
    start = time.perf_counter()

    os.system("COMMAND TO MEASURE THE EXECUTION TIME")

    end = time.perf_counter()
    elapsed = end - start

    print("elapsed time = {:.12f} seconds".format(elapsed))

    ''' 
    elapsed time = 0.000000410520 seconds
    '''

