
import os
from langchain.vectorstores import Chroma
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAI
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_community.retrievers import BM25Retriever

from langchain import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_core.messages import HumanMessage

import torch

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
os.environ['GOOGLE_API_KEY'] = "AIzaSyB3QX46EFHbg_qL5P2QOmxZQMR5_OSCMEI"

def load_vdb(db_path, embedding_function, index_name):
    vdb = Chroma(persist_directory=db_path, collection_name=index_name,
                 embedding_function=embedding_function,collection_metadata={"hnsw:space": "cosine"})
    print("[INFO] load vector database successfull")
    return vdb

def load_embedding_model(model_name, model_kwargs={'device': DEVICE}):
    return HuggingFaceEmbeddings(
        model_name=model_name,
        model_kwargs=model_kwargs,
    )

def get_llm_and_retriever():
    
    try:
        # pdf_dir_path = "elders_care_docs"
        vdb_path = "vector_databases"
        # Path(vdb_path).mkdir(parents=True,exist_ok=True)
        collection_name = "elders_care_expert"
        vdb_path = vdb_path + "/" + collection_name
        
        
        embed_model_name = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"
        embedding_model = load_embedding_model(model_name=embed_model_name)
        
        expert_vdb = load_vdb(
            db_path= vdb_path,
            embedding_function=embedding_model,
            index_name=collection_name,
        )
        
        print("loading expert vector database success")
        
        expert_llm =  GoogleGenerativeAI(
            model="gemini-1.5-pro-latest",
            temperature=0.4,
            top_k=3,
            top_p=0.7,
            max_output_tokens=1000,
            # safety_settings=gemini_safety_settings,
        )
        
        retriever = expert_vdb.as_retriever(search_type="mmr", search_kwargs={'k': 25})
        retriever_from_llm = MultiQueryRetriever.from_llm(
            retriever=retriever, llm=expert_llm
        )
        
        return retriever_from_llm,expert_llm

    except Exception as ex:
        
        print("error in loading expert vector database: ",ex)
        

def retrieve_documents(user_query,retriever):
    retrieved_docs = retriever.invoke(user_query)
        # retrieved_docs = vdb.similarity_search_with_score(user_query, k=3,)
        
    bm25_retriever = BM25Retriever.from_documents(retrieved_docs)
    bm25_retriever.k =  4 # Retrieve top 2 results
    bm25_retrieved_docs = bm25_retriever.invoke(user_query)
    similar_docs = bm25_retrieved_docs
    document_text = [doc.page_content for doc in similar_docs]
    
    print(similar_docs)
    return document_text

PROMPT_TEMPLATE = """
You are a medical expert for suggesting treatment methods based on the provided documents to identified medical requirements to the caregiver.
Your mission is to provide both the treatments we should provide and we should avoid for the identified medical requirements.
You should organize your response in a professional, objective tone. Provide your thought
process to explain how you reasoned to provide the response.

Steps:
1. Read and understand the query and sources thoroughly.
2. Use all sources provided in the document to think about how to provide the correct medical treatments to perform by the caregiver.
3. If the sources in the document are overlapping or have duplicate details, select sources which
are most detailed and comprehensive.
4. Remember to provide both treatments methods what we should do and what we should not do.

Now it's your turn!
<DOCUMENT>
{context}
</DOCUMENT>
<INSTRUCTIONS>
Your response should include a 2-step cohesive answer with following keys:
1. "Thought" key: Explain how you would use the sources in the document to partially or
completely answer the query.
2. "Technical Document":
- Present each treatment method accurately without adding new information.
- Treatment method might include the possible nutrients (meal), physical exercises, mental exercises, etc.
- Avoid mixing facts different areas.
3. Order of keys in the response must be "Thought", and "Technical Document".
4. Double-check compliance with all instructions.
</INSTRUCTIONS>
<QUERY>{query}</QUERY>
OUTPUT:
"""

def generate_suggestions(user_query,expert_llm,retriever,template=None):
    
    retrieved_documents = retrieve_documents(user_query,retriever)
    
    user_prompt = template.format(
        query=user_query,
        context=retrieved_documents
    )
    response = expert_llm.invoke(user_prompt)
    
    return response
        
def main():
    retriever_from_llm,expert_llm = get_llm_and_retriever()
    
    while True:
        
        user_query = input("Patient medical details: ")
        print()
        
        if user_query == "exit":
            break
    
        
        response = generate_suggestions(
            user_query,
            expert_llm,
            retriever=retriever_from_llm,
            template=PROMPT_TEMPLATE
        )
        
        print(response)
        print("-"*100)

if __name__=="__main__":
    main()