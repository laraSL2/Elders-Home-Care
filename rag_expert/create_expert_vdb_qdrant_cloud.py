import os
import sys
import time
from glob import glob
from langchain.text_splitter import RecursiveCharacterTextSplitter

from langchain.vectorstores import Qdrant
from pathlib import Path
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
import torch

import time


from langchain.docstore.document import Document

## to load different extensioned file types
from langchain_community.document_loaders import UnstructuredFileLoader
from unstructured.cleaners.core import clean_extra_whitespace

from langchain_webscraper import retrieve_documents

from qdrant_client import QdrantClient

from dotenv import load_dotenv ## loading the env variables
load_dotenv()


DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

###########
def load_embedding_model(model_name, model_kwargs={'device': DEVICE}):
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
    )

def load_vdb(embedding_function, index_name, delete_collection=False):
    
    client = QdrantClient(
        url = os.environ['QDRANT_URL'],
        api_key = os.environ['QDRANT_API_KEY'],
    )

    ## delete current collection and start with fresh for the same index/collection name
    if delete_collection: 
        client.delete_collection(collection_name=index_name)

    vdb_exist = client.collection_exists(collection_name=collection_name)
    
    vdb = None

    if vdb_exist:
        vdb = Qdrant(
            client=client,
            embeddings=embedding_function,
            collection_name=index_name,
        )
        print("[INFO] load vector database successfull")
    return vdb


def create_and_save_vdb(texts_docs, embedding_function, index_name):
    vdb = Qdrant.from_documents(
        texts_docs,
        embedding_function,
        url=os.environ['QDRANT_URL'],
        prefer_grpc=True,
        api_key=os.environ['QDRANT_API_KEY'],
        collection_name=index_name,
    )

    # vdb.persist()
    # print("[INFO] save the vector dabase")
    return vdb

#########################################################


#########################################################
# functions related to vector embeddings



## process each file path
def process_each_file(item_path,vdb,r_text_splitter,vector_db_path,db_name,embedding_model):
    # take extension
    file_extention = item_path.split(".")[-1]
    print(f"file extention {file_extention}")
    
    loader, splitted_docs = None,None
    
    try:
    
        if file_extention in ["csv","pdf","txt","pptx","docx","xlxs","xls"]:
            loader = UnstructuredFileLoader(item_path,post_processors=[clean_extra_whitespace],)
            splitted_docs = loader.load_and_split(text_splitter=r_text_splitter)
                
            ## Todo: can try to split the documents using recursive splitting method to further split the texts
            
            if len(splitted_docs) > 0:
                
                if vdb is None: ## if vector database is not available create vector database 
                    vdb = create_and_save_vdb(texts_docs=splitted_docs,embedding_function=embedding_model,
                         index_name=db_name
                        )
                else:
                    vdb.add_documents(splitted_docs)
    
    except Exception as ex:
        print(ex)

## process each document
def process_each_doc(doc,vdb,r_text_splitter,db_name,embedding_model):
    # take extension
       
    try:
        #print(type(doc))
        splitted_docs = r_text_splitter.split_documents([doc])
        print(f"splitted: {len(splitted_docs)}")
            
        ## Todo: can try to split the documents using recursive splitting method to further split the texts
        
        if len(splitted_docs) > 0:
            
            if vdb is None: ## if vector database is not available create vector database 
                vdb = create_and_save_vdb(texts_docs=splitted_docs,embedding_function=embedding_model,
                                          index_name=db_name
                    )
            else:
                vdb.add_documents(splitted_docs)
    
    except Exception as ex:
        print(ex)

    finally:
        return vdb
 
def creating_vector_dbs(collection_name,urls=None,save_dir=None):
    try:
        
        # urls = ["https://nurseslabs.com/geriatric-nursing-care-plans/","https://www.betterhealth.vic.gov.au/health/healthyliving/Nutrition-needs-when-youre-over-65","https://www.assistinghands-il-wi.com/blog/foods-good-for-arthritis/"]
        #urls = None
         
        # embed_model_name = "thenlper/gte-small"
        # embed_model_name = "thenlper/gte-large"
        embed_model_name = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"
        embedding_model = load_embedding_model(model_name=embed_model_name)
        r_text_splitter = RecursiveCharacterTextSplitter(separators=['\n'], chunk_size=750, chunk_overlap=150)
        
        docs = None
        if urls:
            docs = retrieve_documents(urls,save_dir=save_dir,character_splitter = None)
            time.sleep(2.0) ## just to make sure it stopped to create the pdfs -> can remove
 
        vdb = None
        try:            
            vdb = load_vdb(embedding_function=embedding_model, index_name=collection_name)
        except Exception as ex_load_vdb:
            
            vdb = None 
            vdb = load_vdb(embedding_function=embedding_model, index_name=collection_name)
            print("load the vdb inside exception")
        
        doc_number = 0
        total_processing_time = 0.

        ### for all the files in a given directory
        start_time = time.time()
        for doc in docs:
            
           
            doc_number += 1
            print(f"processing doc number: {doc_number}/{len(docs)}")
            
            vdb = process_each_doc(
                    doc=doc,
                    vdb = vdb,
                    r_text_splitter = r_text_splitter,

                    db_name = collection_name,
                    embedding_model = embedding_model,
                )
        
        end_time = time.time()
        total_processing_time = end_time - start_time
        print(f"total processing time: {total_processing_time}")
         
        return vdb

    except Exception as ex:
        print(ex)

def deleting_qdrant_collection(collection_name):
    try:
        client = QdrantClient(
            url = os.environ['QDRANT_URL'],
            api_key = os.environ['QDRANT_API_KEY'],
        )

        print(f"Collection {collection_name} exists: {client.collection_exists(collection_name=collection_name)}")
        client.delete_collection(collection_name=collection_name)
        print("Collection deleted")
        print(f"Collection {collection_name} exists after deletion: {client.collection_exists(collection_name=collection_name)}")
    
    except Exception as ex:
        print(f"Exception in deletion of the collection {collection_name}: {ex}") 
        
if __name__=="__main__":

    collection_name = "vdb_elders_home_care"
    documents_save_dir = "rag_expert/docs_from_urls"

    urls = list(set(["https://nurseslabs.com/geriatric-nursing-care-plans/",
            "https://www.betterhealth.vic.gov.au/health/healthyliving/Nutrition-needs-when-youre-over-65",
            "https://www.assistinghands-il-wi.com/blog/foods-good-for-arthritis/",
            "https://www.sandiegohomecaregivers.com/home-care-resources/common-causes-and-supportive-responses-for-alzheimers-related-behaviors/",
            "https://my.clevelandclinic.org/health/diseases/9170-dementia",
            "https://www.agespace.org/health/health-elderly-illnesses/eyesight-health-tips-elderly",
            "https://www.nhs.uk/conditions/urinary-incontinence/",
            "https://www.nhs.uk/conditions/bowel-incontinence/",
            "https://www.agespace.org/health/health-elderly-illnesses/utis",
            "https://www.agespace.org/dementia/help-someone-with-dementia-to-sleep-better",
            "https://www.nhs.uk/conditions/coronary-heart-disease/",
            "https://www.everydayhealth.com/asthma/everyday-guide-to-living-well/"
            ]))
    
    # deleting_qdrant_collection(collection_name)

    creating_vector_dbs(
        collection_name=collection_name,
        urls=urls,
        save_dir=documents_save_dir,
    )