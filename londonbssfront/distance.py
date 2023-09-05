import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt

def dist(lat1, long1, lat2, long2):
    """
Replicating the same formula as mentioned in Wiki
    """
    # convert decimal degrees to radians
    lat1, long1, lat2, long2 = map(radians, [lat1, long1, lat2, long2])
    # haversine formula
    dlon = long2 - long1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    # Radius of earth in kilometers is 6371
    km = 6371* c
    return km


def find_nearest(lat, long,df):
    distances = df.apply(
        lambda row: dist(lat, long, row['s_lat'], row['s_lon']),
        axis=1)
    return df.loc[distances.idxmin(), 'Station_name']
