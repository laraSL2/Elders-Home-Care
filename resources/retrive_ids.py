import sys
import os
from graph_initializer import GraphInitializer
from neo4j import GraphDatabase
import os
import json
from dotenv import load_dotenv
import time
load_dotenv()

uri = os.getenv("NEO4J_URI")
username = os.getenv("NEO4J_USERNAME")
password = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(uri, auth=(username, password))


def getID():
    initializer = GraphInitializer()
    result = initializer.run_query(query="MATCH (e:Elder) RETURN e.id AS ID")
    if result.empty:
        return []
    return result


def run_query(query, parameters=None):
    with driver.session() as session:
        result = session.run(query, parameters)
        return list(result) 

def get_elder_details(elder_id):
    
    cypher_query = "MATCH (e: Elder) WHERE e.id = $elder_id RETURN e AS details"
    # cypher_query = """
    # MATCH (e:Elder {id: 'e0002'})-[r]->(n)
    # RETURN e, r, n
    # """
    parameters = {"elder_id": elder_id}
    # cypher_query = """MATCH (elder:Elder {id: 'e0001'})-[r*]-(related)
    # RETURN elder, collect(related) AS relatedNodes, collect(r) AS details"""
    # Run the query and convert the result to JSON format
    start_query_time = time.time()

    results = run_query(cypher_query, parameters)
    
    end_query_time = time.time()
    # Calculate the total query execution time
    query_time = end_query_time - start_query_time

    print(f"Query execution time: {query_time} seconds")

    print(results)
    json_result = []
    for record in results:
        node_properties = dict(record['details'].items())
        json_result.append(node_properties)
    
    return json.dumps(json_result, indent=4)



# details = get_elder_details('e0001')
# print(details)
# print(getID())