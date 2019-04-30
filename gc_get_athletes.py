"""
Fetch GC Open Data athletes, who have >100 RIDES after 2015
"""

START_DATE = '2015-01-01'
N_RIDES = 100


from opendata import OpenData
import pandas as pd
import maya


od = OpenData()

atl = od.remote_athletes()


min_time = maya.parse(START_DATE).datetime(naive=False)

for a in atl:
    timestr = list(a.metadata['RIDES'].keys())
    timeiso8601 = [maya.parse(t).iso8601() for t in timestr]
    if (pd.to_datetime(timeiso8601).min()<min_time) & (len(timeiso8601)>N_RIDES):
        a.store_locally(data=False)
        print('{} rides {}'.format(a.metadata['ATHLETE']['id'], len(timeiso8601)))