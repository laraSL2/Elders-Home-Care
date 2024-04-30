import re
from string import Template
import json
import datetime
import random
from prompts import Prompts
from graph_initializer import GraphInitializer

def clean_text(text):
    return re.sub(r'[^\x00-\x7F]+',' ', text)

def extractor(elderID, gemini, care_note_mode, data="", care_note=""):
  results = {"entities": [], "relationships": []}

  extracting_prompts = Prompts()
  prompts = [extracting_prompts.eld_cons_res_prompt, 
             extracting_prompts.con_dis_drug_food_prompt, 
             extracting_prompts.mon_obs_docshe_prompt, 
             extracting_prompts.adl_iadl_cog_soc_prompt]
  for id, p in enumerate(prompts):
      try:
        if care_note_mode:
          _prompt = Template(p).substitute(ctext=clean_text(care_note))
        else:
          _prompt = Template(p).substitute(ctext=clean_text(data))
        _extraction = gemini.extract_entities_relationships(_prompt, 'gemini-pro')
        print(_extraction)
        if 'Answer:\n' in _extraction:
            _extraction = _extraction.split('Answer:\n ')[1]
        if _extraction.strip() in ['', 'N/A', 'null'] :
            continue
        try:
            _extraction = json.loads(_extraction.replace("\'", "'").replace('`', ''))
        except json.JSONDecodeError:
            # print(_extraction)
            #Temp hack to ignore Skills cut off by token limitation
            # _extraction = _extraction[:_extraction.rfind("}")+1] + ']}'
            _extraction = _extraction.replace("json","").replace("\n","").replace("`","")
            _extraction = json.loads(_extraction.replace("\'", '"').replace("'", '"').replace("None", "null"))
        results["entities"].extend(_extraction["entities"])
        if "relationships" in _extraction:
            results["relationships"].extend(_extraction["relationships"])
      except:
        print(f"extraction error occured in prompt {id}")
  if care_note_mode:
      current_date = datetime.date.today()
      current_date_str = current_date.strftime("%Y-%m-%d")
      results["entities"].append({"label":"Care_Note", "id":f'{elderID}_{current_date_str}',"note": care_note, "date": current_date_str})
      results["relationships"].append(f'{elderID}|HAS_CARENOTE|{elderID}_{current_date_str}')
      results["entities"] = [d for d in results["entities"] if d.get('label') not in ['Elder']]
  return results


def add_essential_nodes(elderID, results, care_note_mode=False):
  current_date = datetime.date.today()
  current_date_str = current_date.strftime("%Y-%m-%d")
  if care_note_mode:
    results["entities"].append({'label': 'Encounter', 'id': f'{elderID}_encounter', 'updated_at': current_date_str})
    return results

  elder_found = False
  encounter_found = False
  condition_found = False
  for e in results['entities']:
    if e["label"] == 'Elder':
      e["id"] = elderID
      elder_found = True
    if e["label"] == 'Encounter':
      e["id"] = f'{elderID}_encounter'
      encounter_found = True
    if e["label"] == 'Condition':
      e["id"] = f'{elderID}_condition'
      condition_found = True

  if not elder_found:
    raise ValueError("Elder does not extracted")

  if not encounter_found:
    results["entities"].append({'label': 'Encounter',
    'id': f'{elderID}_encounter',
    'updated_at': current_date_str,
    'created_at': current_date_str})
    results["relationships"].append(f"{elderID}|HAS_ENCOUNTER|{elderID}_encounter")

  if not condition_found:
    results["entities"].append( {'label': 'Condition',
    'id': f'{elderID}_condition',
    'symptoms': [],
    'past_diseases': [],
    'past_surgeries': [],
    'description': ''})
  return results


def add_relationships(results, elderID):
  encounter_id = f'{elderID}_encounter'
  condition_id = f'{elderID}_condition'
  for e in results["entities"]:
      if e['label'] == 'Social_History':
          results["relationships"].append(f"{elderID}|HAS_SOCIAL_HISTORY|{e['id']}")
      if e['label'] == 'Education':
          results["relationships"].append(f"{elderID}|HAS_EDUCATION|{e['id']}")
      if e['label'] == 'Previous_Consultant':
          results["relationships"].append(f"{elderID}|HAD_CONSULTANT|{e['id']}")
      if e['label'] == 'Previous_Residence':
          results["relationships"].append(f"{elderID}|HAD_RESIDENCE|{e['id']}")
      if e['label'] == 'Condition':
          results["relationships"].append(f"{encounter_id}|HAS_CONDITION|{e['id']}")
      if e['label'] == 'Disease':
          results["relationships"].append(f"{condition_id}|HAS_DISEASE|{e['id']}")
      if e['label'] == 'Drug':
          results["relationships"].append(f"{condition_id}|HAS_DRUG|{e['id']}")
      if e['label'] == 'Observation':
          results["relationships"].append(f"{encounter_id}|HAS_OBSERVATION|{e['id']}")
      if e['label'] == 'Food':
        if e['allergy'] == "True" or  e['allergy'] == True:
          results["relationships"].append(f"{elderID}|HAS_ALLERGY|{e['id']}")
        if e['prefer'] == "True" or e['prefer'] == True:
          results["relationships"].append(f"{elderID}|HAS_PREFERENCE|{e['id']}")
      if e['label'] == 'Monitoring_Plan':
          results["relationships"].append(f"{encounter_id}|HAS_MONITORING_PLAN|{e['id']}")
      if e['label'] == 'Doctor_Scheduled':
        results["relationships"].append(f"{encounter_id}|HAS_DOCTOR_SCHEDULED|{e['id']}")
      if e['label'] == 'ADL':
        results["relationships"].append(f"{encounter_id}|NEED_ADL_ASSISTANCE|{e['id']}")
      if e['label'] == 'IADL':
        results["relationships"].append(f"{encounter_id}|NEED_IADL_ASSISTANCE|{e['id']}")
      if e['label'] == 'Cognitive_Assessment':
        results["relationships"].append(f"{encounter_id}|HAS_COGNITIVE_ASSESSMENT|{e['id']}")
  return results


"""## Data Ingestion Cypher Generation

The entities and relationships we got from the LLM have to be transformed to Cypher so we can write them into Neo4j.
"""

nodes = ['Elder', 'Previous_Consultant', 'Previous_Residence', 'Condition', 'Social_History', 'Disease', 'Drug', 'Monitoring_Plan', 'Observation', 'Food', 'Doctor_Scheduled', 'Encounter', 'ADL', 'IADL', 'Care_Note', "Cognitive_Assessment"]
relationships = ['HAD_CONSULTANT', 'HAD_RESIDENCE', 'HAS_ENCOUNTER', 'HAS_SOCIAL_HISTORY', 'HAS_CONDITION', 'HAS_MONITORING_PLAN', 'HAS_DISEASE', 'HAS_DRUG', 'HAS_OBSERVATION', 'HAS_DOCTOR_SCHEDULED', 'NEEDS_OBSERVATION', 'NEEDS_MONITORING', 'HAS_PREFERENCE', 'HAS_ALLERGY', 'NOT_RECOMMENDED', 'RECOMMENDED', 'NEED_ADL_ASSISTANCE', 'NEED_IADL_ASSISTANCE', 'HAS_CARENOTE',"HAS_COGNITIVE_ASSESSMENT"]


def id_generator(elderID, j): # Social History, Mon_plan, Observation,
  label = j["label"]
  label_idx = nodes.index(label)
  try:
    if label == "Elder":
      id = elderID
    elif label == "Encounter":
      id = f'{elderID}_encounter'
    elif label == "Condition":
      id = f'{elderID}_condition'
    elif label == "Social_History":
      id = f'{elderID}_social'
    elif label in ["Previous_Consultant", "Previous_Residence", "Disease", "Drug", "Food",]:
      name = j["name"].replace(" ","")
      id = f'{elderID}_{label_idx}{name}'
    elif label == "Doctor_Scheduled":
      doc_name, app_date = j["doctor_name"].replace(" ",""), j["appoinment_date"].replace(" ","")
      id = f'{elderID}_{label_idx}{doc_name}{app_date}'
    elif label in ["ADL", "IADL", "Cognitive_Assessment", "Observation", "Monitoring_Plan"]:
      ran_num = random.randint(1000000, 9999999)
      id = f'{elderID}_{label_idx}_{ran_num}'
    elif label == "Care_Note":
      id_generated = j['id']
      id = f'{id_generated}'
    else:
      id_generated = j['id']
      id = f'{label_idx}_{elderID}_{id_generated}'
  except:
    print("Error Occured. Using Generated ID...")
    id_generated = j['id']
    id = f'{label_idx}_{elderID}_{id_generated}'
  return id


def get_prop_str(prop_dict, _id):
    s = []
    for key, val in prop_dict.items():
      if key != 'label' and key != 'id':
         s.append(_id+"."+key+' = "'+str(val).replace('\"', '"').replace('"', '\"')+'"')
    return ' ON CREATE SET ' + ','.join(s)

def get_update_str(prop_dict, _id):
    s = []
    for key, val in prop_dict.items():
        if key != 'label' and key != 'id':
            value = '"'+str(val).replace('\"', '"').replace('"', '\"')+'"'
            s.append(f'{key}: {value}')
    match_stmnt = f'MATCH (n:{prop_dict["label"]}) WHERE n.id = "{_id}"'
    return f'{match_stmnt} SET n += {{{",".join(s)}}}'

def get_cypher_compliant_var(_id):
    s = "_"+ re.sub(r'[\W_]', '', _id).lower() #avoid numbers appearing as firstchar; replace spaces
    return s[:20] #restrict variable size

def generate_cypher(elderID, in_json):
    e_map = {}
    e_stmt = []
    r_stmt = []
    e_stmt_tpl = Template("($id:$label{id:'$key'})")
    r_stmt_tpl = Template("""
      MATCH $src
      MATCH $tgt
      MERGE ($src_id)-[:$rel]->($tgt_id)
    """)
    for obj in in_json:
      for j in obj['entities']:
          props = ''
          label = j['label']
          id = ''
          id = id_generator(elderID, j)

          if label in nodes:
            varname = get_cypher_compliant_var(j['id'])
            stmt = e_stmt_tpl.substitute(id=varname, label=label, key=id)
            e_map[varname] = stmt
            prop_str = get_prop_str(j, varname)
            update_str = get_update_str(j, id)
            e_stmt.append('MERGE '+ stmt + prop_str)
            e_stmt.append(update_str)
      for st in obj['relationships']:
          rels = st.split("|")
          src_id = get_cypher_compliant_var(rels[0].strip())
          rel = rels[1].strip()
          if rel in relationships: #we ignore other relationships
            tgt_id = get_cypher_compliant_var(rels[2].strip())
            if rel == 'HAS_CARENOTE':
              src = "(_"+elderID+":Elder{id:'"+elderID+"'})"
              stmt = r_stmt_tpl.substitute(
                src_id=src_id, tgt_id=tgt_id, src=src, tgt=e_map[tgt_id], rel=rel)
            else:
              print(e_map)
              print(src_id, tgt_id, rel)
              stmt = r_stmt_tpl.substitute(
                src_id=src_id, tgt_id=tgt_id, src=e_map[src_id], tgt=e_map[tgt_id], rel=rel)
            r_stmt.append(stmt)

    return e_stmt, r_stmt


"""## Pipeline"""

def add_patient(gemini, graph, elderid, care_note_mode=False, care_note="", data=""):
    graph.define_nodes_uniqueness()
    # try:
    print("Elder ID: ", elderid)
    print(f"    Extracting Entities & Relationships")
    results = extractor(elderid, gemini, care_note_mode, data=data, care_note=care_note)
    results = add_essential_nodes(elderid, results, care_note_mode)
    results = add_relationships(results, elderid)
    print(f"    Generating Cypher")
    ent_cyp, rel_cyp = generate_cypher(elderid, [results])
    print(f"    Ingesting Entities")
    for e in ent_cyp:
        graph.run_query(e)
    print(f"    Ingesting Relationships")
    for r in rel_cyp:
        graph.run_query(r)
    print(f"    Processing DONE")
    return True
    # except Exception as e:
    #     print(f"    Processing Failed with exception {e}")
    #     return False

def get_max_patient_id(graph):
    query = "MATCH (e:Elder) RETURN max(toInteger(substring(e.id, 1))) AS max_id"
    result = graph.run_query(query)
    return result['max_id'][0]

def get_next_patient_id(graph):
    max_id = get_max_patient_id(graph)
    if max_id is None:
        return ""
    return "e"+str(max_id + 1).zfill(4)
