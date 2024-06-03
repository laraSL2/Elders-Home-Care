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


DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'

###########
def load_embedding_model(model_name, model_kwargs={'device': DEVICE}):
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
    )

def load_vdb(embedding_function, index_name):
    
    client = QdrantClient(
        os.environ['QDRANT_URL'],
        os.environ['QDRANT_API_KEY'],
    )
    
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
                        db_path=vector_db_path, index_name=db_name
                        )
                else:
                    vdb.add_documents(splitted_docs)
    
    except Exception as ex:
        print(ex)

## process each document
def process_each_doc(doc,vdb,r_text_splitter,vector_db_path,db_name,embedding_model):
    # take extension
       
    try:
        
        splitted_docs = r_text_splitter.split(doc)
            
        ## Todo: can try to split the documents using recursive splitting method to further split the texts
        
        if len(splitted_docs) > 0:
            
            if vdb is None: ## if vector database is not available create vector database 
                vdb = create_and_save_vdb(texts_docs=splitted_docs,embedding_function=embedding_model,
                    db_path=vector_db_path, index_name=db_name
                    )
            else:
                vdb.add_documents(splitted_docs)
    
    except Exception as ex:
        print(ex)
 
def creating_vector_dbs(docs,collection_name,urls=None):
    try:
        
       
        
        # urls = ["https://nurseslabs.com/geriatric-nursing-care-plans/","https://www.betterhealth.vic.gov.au/health/healthyliving/Nutrition-needs-when-youre-over-65","https://www.assistinghands-il-wi.com/blog/foods-good-for-arthritis/"]
        #urls = None
         
        # embed_model_name = "thenlper/gte-small"
        # embed_model_name = "thenlper/gte-large"
        embed_model_name = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"
        embedding_model = load_embedding_model(model_name=embed_model_name)
        r_text_splitter = RecursiveCharacterTextSplitter(separators=['\n'], chunk_size=750, chunk_overlap=150)
        
        
        if urls:
            retrieve_documents(urls,save_dir=None,character_splitter = None)
            time.sleep(5.0) ## just to make sure it stopped to create the pdfs -> can remove
 
        vdb = None
        try:            
            vdb = load_vdb(embedding_function=embedding_model, index_name=collection_name)
        except Exception as ex_load_vdb:
            vdb = None 
        
        doc_number = 1
        total_processing_time = 0.

        ### for all the files in a given directory
        start_time = time.time()
        for doc in docs:
            
           
            doc_number += 1
            print(f"processing doc number: {doc_number}")
            
            process_each_doc(
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
        
if __name__=="__main__":
    creating_vector_dbs()