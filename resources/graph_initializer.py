"""## Data Ingestion"""
import os
from neo4j import GraphDatabase
import pandas as pd
import json
from dotenv import load_dotenv

class GraphInitializer:
  def __init__(self, config_path="config.json"):
    load_dotenv()
    # with open(config_path) as f:
    #   config = json.load(f)
    # self.connectionUrl = config["neo4j-url"]
    # self.username = config["neo4j-user"]
    # self.password = config["neo4j-password"]


    self.connectionUrl = os.getenv("NEO4J_URI")
    self.username = os.getenv("NEO4J_USERNAME")
    self.password = os.getenv("NEO4J_PASSWORD")
    self.driver = GraphDatabase.driver(self.connectionUrl, auth=(self.username, self.password))
    self.driver.verify_connectivity()
    print("Initializing the graph")

  def run_query(self, query, params={}):
      with self.driver.session() as session:
          result = session.run(query, params)
          return pd.DataFrame([r.values() for r in result], columns=result.keys())

  def define_nodes_uniqueness(self):
    self.run_query('CREATE CONSTRAINT unique_patient_id IF NOT EXISTS FOR (n:Patient) REQUIRE (n.id) IS UNIQUE')
    self.run_query('CREATE CONSTRAINT unique_previous_consultant_id IF NOT EXISTS FOR (n:Previous_Consultant) REQUIRE (n.id) IS UNIQUE')
    self.run_query('CREATE CONSTRAINT unique_previous_residence_id IF NOT EXISTS FOR (n:Previous_Residence) REQUIRE n.id IS UNIQUE')
    self.run_query('CREATE CONSTRAINT unique_condition_id IF NOT EXISTS FOR (n:Condition) REQUIRE n.id IS UNIQUE')
    self.run_query('CREATE CONSTRAINT unique_social_history_id IF NOT EXISTS FOR (n:Social_History) REQUIRE n.id IS UNIQUE')
    self.run_query('CREATE CONSTRAINT unique_disease_id IF NOT EXISTS FOR (n:Disease) REQUIRE (n.id) IS UNIQUE')
    self.run_query('CREATE CONSTRAINT unique_drug_id IF NOT EXISTS FOR (n:Drug) REQUIRE (n.id) IS UNIQUE')
    self.run_query('CREATE CONSTRAINT unique_monitoring_plan_id IF NOT EXISTS FOR (n:Monitoring_Plan) REQUIRE n.id IS UNIQUE')
    self.run_query('CREATE CONSTRAINT unique_observation_id IF NOT EXISTS FOR (n:Observation) REQUIRE n.id IS UNIQUE')
    self.run_query('CREATE CONSTRAINT unique_food_id IF NOT EXISTS FOR (n:Food) REQUIRE n.id IS UNIQUE')
    self.run_query('CREATE CONSTRAINT unique_doctor_scheduled_id IF NOT EXISTS FOR (n:Doctor_Scheduled) REQUIRE (n.id) IS UNIQUE')
    self.run_query('CREATE CONSTRAINT unique_encounter_id IF NOT EXISTS FOR (n:Encounter) REQUIRE (n.id) IS UNIQUE')
    self.run_query('CREATE CONSTRAINT unique_adl_id IF NOT EXISTS FOR (n:ADL) REQUIRE n.id IS UNIQUE')
    self.run_query('CREATE CONSTRAINT unique_iadl_id IF NOT EXISTS FOR (n:IADL) REQUIRE n.id IS UNIQUE')
    self.run_query('CREATE CONSTRAINT unique_care_note_id IF NOT EXISTS FOR (n:Care_Note) REQUIRE n.id IS UNIQUE')