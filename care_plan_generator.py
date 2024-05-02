"""# Extracting information from the KG"""

from typing import List, Dict
from neo4j import graph
from datetime import datetime, timedelta
from graph_initializer import GraphInitializer
from gemini_initializer import GeminiInitializer
from prompts import Prompts

class GetDetailsFromKG:
    def __init__(self, Nodes: graph.Node, Relationships: graph.Relationship)->None:
        self.nodes = Nodes
        self.relationships = Relationships

    def del_id(self, dictionary):
        dictionary.pop("id", None)
        return(dictionary)

    def person_details(self)->Dict:
        elder_node = [node for node in self.nodes if list(node.labels)[0]=='Elder'][0]
        elder_properties = self.del_id(dict(elder_node.items()))
        keys_to_delete = ["guardian_name", "guardian_contact", "blood_type", "weight", "height", "bmi", "marital_status","hobbies"]

        for key in keys_to_delete:
            if key in elder_properties:
                del elder_properties[key]
        print("elder properties: ", elder_properties)
        return elder_properties

    def social_history(self)->Dict:
        social_history_node = [node for node in self.nodes if list(node.labels)[0]=='Social_History']
        social_history_properties = {}
        if len(social_history_node) != 0:
            social_history_node = social_history_node[0]
            social_history_properties = self.del_id(dict(social_history_node.items()))
        previous_residence_nodes = [node for node in self.nodes if list(node.labels)[0]=='Previous_Residence']
        previous_residence_properties = [self.del_id(dict(node.items())) for node in previous_residence_nodes]
        social_history = {}
        social_history["social_history"] = social_history_properties
        social_history["previous_residence"] = previous_residence_properties
        print("social history: ", social_history)
        return social_history

    def medical_history(self)->Dict:
        condition_node = [node for node in self.nodes if list(node.labels)[0]=='Condition'][0]
        previous_consultant_nodes = [node for node in self.nodes if list(node.labels)[0]=='Previous_Consultant']
        condition_properties = self.del_id(dict(condition_node.items()))
        previous_consultant_properties = [self.del_id(dict(node.items())) for node in previous_consultant_nodes]
        medical_history_properties = {}
        medical_history_properties["condition"] = condition_properties
        medical_history_properties["previous_consultant"] = previous_consultant_properties
        print("medical history: ", medical_history_properties)
        return medical_history_properties

    def functional_status(self)->Dict:
        ADL_nodes = [node for node in self.nodes if list(node.labels)[0]=='ADL']
        IADL_nodes = [node for node in self.nodes if list(node.labels)[0]=='IADL']
        Cognitive_nodes = [node for node in self.nodes if list(node.labels)[0]=='Cognitive_Assessment']
        ADL_properties = [self.del_id(dict(node.items())) for node in ADL_nodes]
        IADL_Properties = [self.del_id(dict(node.items())) for node in IADL_nodes]
        Cognitive_properties = [self.del_id(dict(node.items())) for node in Cognitive_nodes]
        functional_status = {}
        functional_status["ADL"] = ADL_properties
        functional_status["IADL"] = IADL_Properties
        functional_status["Cognitive"] = Cognitive_properties
        print("functional status: ", functional_status)
        return functional_status

    def outings(self)->Dict:
        elder_node = [node for node in self.nodes if list(node.labels)[0]=='Elder'][0]
        care_nodes = [node for node in self.nodes if list(node.labels)[0]=='Care_Note']
        hobbies = elder_node["hobbies"]
        care_properties = [self.del_id(dict(node.items())) for node in care_nodes]
        outings_properties = {}
        outings_properties["hobbies"] = hobbies
        outings_properties["care_notes"] = care_properties
        print("outings: ", outings_properties)
        return outings_properties

    def diseases(self)->List[Dict]:
        disease_nodes = [node for node in self.nodes if list(node.labels)[0]=='Disease']
        disease_properties = []
        for node in disease_nodes:
            disease_element_id = node.element_id
            drugs_nodes = [relationship.end_node for relationship in self.relationships if relationship.start_node.element_id==disease_element_id and list(relationship.end_node.labels)[0] == "Drug"]
            drugs_properties = [self.del_id(dict(drugnode.items())) for drugnode in drugs_nodes]
            drugs_names = [drug["name"] for drug in drugs_properties]
            disease_property = self.del_id(dict(node.items()))
            disease_property["relevent drugs"] = drugs_names
            disease_properties.append(disease_property)
        print("diseases: ", disease_properties)
        return disease_properties

    def medication(self)->List[Dict]:
        medication_nodes = [node for node in self.nodes if list(node.labels)[0]=='Drug']
        medication_properties = []
        for node in medication_nodes:
            medication_properties.append(self.del_id(dict(node.items())))
        print("medication: ", medication_properties)
        return medication_properties

    def dietry_plan(self)->Dict:
        prefer_foods_nodes = [relationship.end_node for relationship in self.relationships if relationship.type=='HAS_PREFERENCE']
        allergy_foods_nodes = [relationship.end_node for relationship in self.relationships if relationship.type=='HAS_ALLERGY']
        recommended_foods_disease_nodes = [(relationship.start_node, relationship.end_node) for relationship in self.relationships if relationship.type=='RECOMMENDED']
        not_recommended_foods_disease_nodes = [(relationship.start_node, relationship.end_node) for relationship in self.relationships if relationship.type=='NOT_RECOMMENDED']
        prefer_foods_properties = [self.del_id(dict(node.items())) for node in prefer_foods_nodes]
        prefer_foods_properties = [{"name":food["name"], "description":food["description"]} for food in prefer_foods_properties]
        allergy_foods_properties = [self.del_id(dict(node.items())) for node in allergy_foods_nodes]
        allergy_foods_properties = [{"name":food["name"], "description":food["description"]} for food in allergy_foods_properties]
        recommended_foods_disease_properties = [(self.del_id(dict(node1.items())), self.del_id(dict(node2.items()))) for node1, node2 in recommended_foods_disease_nodes]
        not_recommended_foods_disease_properties = [(self.del_id(dict(node1.items())), self.del_id(dict(node2.items()))) for node1, node2 in not_recommended_foods_disease_nodes]
        recommended, not_recommended = [], []
        for node1, node2 in recommended_foods_disease_properties:
            recommended.append({"disease":node1["name"], "recommended_food": node2["name"]})
        for node1, node2 in not_recommended_foods_disease_properties:
            not_recommended.append({"disease":node1["name"], "not_recommended_food": node2["name"]})
        dietry_plan = {}
        dietry_plan["prefer_foods"] = prefer_foods_properties
        dietry_plan["allergy_foods"] = allergy_foods_properties
        dietry_plan["recommended_foods"] = recommended
        dietry_plan["not_recommended_foods"] = not_recommended
        print("dietry plan: ", dietry_plan)
        return dietry_plan

    def observation_and_monitoring(self)->Dict:
        observation_nodes = [node for node in self.nodes if list(node.labels)[0]=='Observation']
        monitoring_nodes = [node for node in self.nodes if list(node.labels)[0]=='Monitoring_Plan']
        observation_properties = [self.del_id(dict(node.items())) for node in observation_nodes]
        monitoring_properties = [self.del_id(dict(node.items())) for node in monitoring_nodes]
        observation_and_monitoring = {}
        observation_and_monitoring["observation"] = observation_properties
        observation_and_monitoring["monitoring"] = monitoring_properties
        print("observation and monitoring: ", observation_and_monitoring)
        return observation_and_monitoring

    def doctor_schedules(self)->List[Dict]:
        doctor_nodes = [node for node in self.nodes if list(node.labels)[0]=='Doctor_Scheduled']
        doctor_schedules = []
        for node in doctor_nodes:
            doctor_property = self.del_id(dict(node.items()))
            doctor_element_id = node.element_id
            observation_nodes_properties = [self.del_id(dict(relationship.end_node.items())) for relationship in self.relationships if relationship.start_node.element_id==doctor_element_id and relationship.type=='NEEDS_OBSERVATION']
            monitoring_nodes_properties = [self.del_id(dict(relationship.end_node.items())) for relationship in self.relationships if relationship.start_node.element_id==doctor_element_id and relationship.type=='NEEDS_MONITORING']
            doctor_property["needed_observations"] = observation_nodes_properties
            doctor_property["needed_monitoring_plans"] = monitoring_nodes_properties
            doctor_schedules.append(doctor_property)
        print("doctor schedules: ", doctor_schedules)
        return doctor_schedules

    def care_notes(self, duration_in_weeks = 0)->List[Dict]:
        care_note_nodes = [node for node in self.nodes if list(node.labels)[0]=='Care_Note']
        if duration_in_weeks != 0:
            starting_date = datetime.now() - timedelta(weeks=duration_in_weeks)
            filtered_care_nodes = [node for node in care_note_nodes if datetime.strptime(node['date'], '%Y-%m-%d')>starting_date]
        else:
            filtered_care_nodes = care_note_nodes
        care_note_properties = [self.del_id(dict(node.items())) for node in filtered_care_nodes]
        print("care notes: ", care_note_properties)
        return care_note_properties


def read_graph(elderID: str, GraphInitializer = GraphInitializer())->tuple[graph.Node, graph.Relationship]:
    df = GraphInitializer.run_query("""match p=(n{id:'"""+elderID+"""'})-[*]-() with n, collect(nodes(p)) as listOflistOfnodes, collect(relationships(p)) as listOfListOfrelationships unwind listOflistOfnodes as list unwind list as element with n, collect(distinct element) as distinctNodes, listOfListOfrelationships unwind listOfListOfrelationships as list unwind list as element return distinctNodes, collect(distinct element) as distinctRelationships""")
    if df.empty:
        return [], []
    Nodes = df["distinctNodes"][0]
    Relationships = df['distinctRelationships'][0]
    return Nodes, Relationships

def generate_plan(elderID:str, GeminiInitializer = GeminiInitializer(), GraphInitializer = GeminiInitializer())->str:
    elderID = elderID.lower()
    try:
        Nodes, Relationships = read_graph(elderID, GraphInitializer=GraphInitializer)
    except:
        return "Can Not retrieve Information from the Knowledge Graph. Please update the the transmission capacity."
    elder_node = [node for node in Nodes if list(node.labels)[0]=='Elder']
    if len(elder_node) == 0:
        return "Elder ID not found in the Knowledge Graph"
    kg_details = GetDetailsFromKG(Nodes,Relationships)

    elder_data = str(kg_details.person_details())
    social_history = str(kg_details.social_history())
    medical_history = str(kg_details.medical_history())
    functional_status = str(kg_details.functional_status())
    outings = str(kg_details.outings())
    disease_data = str(kg_details.diseases())
    drug_data = str(kg_details.medication())
    dietary_plan = str(kg_details.dietry_plan())
    monitoring_plan = str(kg_details.observation_and_monitoring())
    doctor_schedule = str(kg_details.doctor_schedules())
    care_notes = str(kg_details.care_notes())


    """## Prompting the LLM to generate the Care Plan"""
    prompt = Prompts()
    plan_prompt = prompt.plan_prompt(elderID, elder_data, social_history, medical_history, functional_status, outings, disease_data, drug_data, dietary_plan, monitoring_plan, doctor_schedule, care_notes)

    _extraction = GeminiInitializer.extract_entities_relationships(plan_prompt,model_name="gemini-1.5-pro-latest")
    return _extraction