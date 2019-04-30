"""
Fetch GC Open Data athletes, who have >100 RIDES after 2015
"""

from opendata import OpenData
import pandas as pd
import maya
import bonobo


START_DATE = '2015-01-01'
N_RIDES = 100

min_time = maya.parse(START_DATE).datetime(naive=False)


def extract():
    """Load athletes from the Golden Cheetah Open Data"""
    od = OpenData()
    remote_atl = od.remote_athletes() # list remote athletes
    local_atl = od.local_athletes() # list athletes locally stored on
    for a in remote_atl:
        if a not in local_atl: # only return the athletes that are not stored locally
            yield a


def transform(a):
    """Return athlete if it has more than N_RIDES after the START_DATE"""
    timestr = list(a.metadata['RIDES'].keys())
    timeiso8601 = [maya.parse(t).iso8601() for t in timestr]
    if (pd.to_datetime(timeiso8601).min()<min_time) & (len(timeiso8601)>N_RIDES):
        print('{} rides {}'.format(a.metadata['ATHLETE']['id'], len(timeiso8601)))
        yield a 


def load(a):
    """Store the athlete locally"""
    a.store_locally(data=False)


def build_graph():
    graph = bonobo.Graph()
    graph.add_chain(extract, transform)
    return graph


if __name__ == "__main__":
    g = build_graph()
    bonobo.run(g)