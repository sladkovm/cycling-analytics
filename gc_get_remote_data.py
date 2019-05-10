"""
Fetch rides from GC Open Data athletes
"""

from opendata import OpenData
import pandas as pd
import maya
import bonobo
from loguru import logger


def extract():
    od = OpenData()
    atl = od.local_athletes()
    for a in atl:
        logger.debug(a.id)
        yield a


def load(a):
    a.download_remote_data()


def build_graph():
    graph = bonobo.Graph()
    graph.add_chain(extract, load)
    return graph


if __name__ == "__main__":
    g = build_graph()
    bonobo.run(g)