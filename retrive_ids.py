import sys
import os
from graph_initializer import GraphInitializer

def getID():
    initializer = GraphInitializer()
    result = initializer.run_query(query="MATCH (e:Elder) RETURN e.id AS ID")
    if result.empty:
        return []
    id_container = []
    for recoer in result:
        id_container.append(recoer)
    return result

