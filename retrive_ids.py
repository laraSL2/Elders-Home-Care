import sys
import os
from graph_initializer import GraphInitializer
from neo4j import GraphDatabase
import os
import json
from dotenv import load_dotenv

load_dotenv()

uri = os.getenv("neo4j-url")
username = os.getenv("neo4j-user")
password = os.getenv("neo4j-password")

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
    parameters = {"elder_id": elder_id}
    # cypher_query = """MATCH (elder:Elder {id: 'e0001'})-[r*]-(related)
    # RETURN elder, collect(related) AS relatedNodes, collect(r) AS details"""
    # Run the query and convert the result to JSON format
    results = run_query(cypher_query, parameters)
    print(results)
    json_result = []
    for record in results:
        node_properties = dict(record['details'].items())
        json_result.append(node_properties)
    
    return json.dumps(json_result, indent=4)



# details = get_elder_details('e0001')
# print(details)
# print(getID())