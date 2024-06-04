
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

from qdrant_client import QdrantClient
from langchain.vectorstores import Qdrant

from dotenv import load_dotenv
load_dotenv()

DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'



def load_vdb(embedding_function, index_name):
    
    client = QdrantClient(
        os.environ['QDRANT_URL'],
        api_key=os.environ['QDRANT_API_KEY'],
    )
    
    vdb = Qdrant(
        client=client,
        embeddings=embedding_function,
        collection_name=index_name,
    )
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
        #vdb_path = "vector_databases"
        # Path(vdb_path).mkdir(parents=True,exist_ok=True)
        collection_name = "vdb_elders_home_care"
        #vdb_path = vdb_path + "/" + collection_name
        
        
        embed_model_name = "sentence-transformers/multi-qa-MiniLM-L6-cos-v1"
        embedding_model = load_embedding_model(model_name=embed_model_name)
        
        expert_vdb = load_vdb(
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
        
        print(expert_vdb)
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
    bm25_retriever.k =  10 # Retrieve top 2 results
    bm25_retrieved_docs = bm25_retriever.invoke(user_query)
    similar_docs = bm25_retrieved_docs
    document_text = [doc.page_content for doc in similar_docs]
    
    print(similar_docs)
    return document_text

PROMPT_TEMPLATE = """
You are a medical expert for suggesting treatment methods based on the provided documents to identified medical requirements in the query to the caregiver.
Your mission is to provide both the treatments we should provide and we should avoid for the identified medical requirements.
You should organize your response in a professional, objective tone. Provide your thought
process to explain how you reasoned to provide the response.


Steps:
1. Read and Analyze the given query comprehensively and identify the medical requirements including care needs if there are any like dimentia, arthuritis, alzhemizer, diabetes, etc.
1. Read and understand the information in documents thoroughly for the identified medical requirements and care needs.
2. ONLY IF REQUIRED , use all information provided in the document to think about how to provide the correct medical treatments to perform by the caregiver. Here please consider the proper medical treatments which the elder might like to do using the provided query.
3. If the information in the document are overlapping or have duplicate details, select information which are most detailed and comprehensive which most similar to provided query details. However, if the details provided in the query for the elder seems fine means the elder seems healthy, you must not provide \
unnecessary information (care needs) or treatments as suggestions.
4. Remember to provide both treatments methods what we should do and what we should not do. Again, do not provide any unnecessary treatments to the elder if you can consider the elder is doing fine from the provided details in the query.

Now it's your turn!

<DOCUMENT>
{context}s
</DOCUMENT>
<INSTRUCTIONS>
Your response should include a 2-step cohesive answer with following keys:
1. "Thought" key: Explain how you would use the information in the document to partially or
completely answer the query. Your thought process includes that why do you suggest the treatment methods based on the preference of the elder and thoughroghly referring \
to the information in the document. However, you should not provide the treatment methods which are not related to the document for the analysed condition for the provided query and any treatment, activity \
    or food type which cause any harm to the elder even if elder likes to do them.
2. "Technical Document":
- Present each treatment method accurately without adding new information but explain in detail why you need to give this treatment (food, medicine, activity, tools, etc.) based on the elders conditions.
- Treatment method might include the possible nutrients (meal), physical exercises, mental exercises, proper care giver tools, etc. While suggesting the treatment methods, consider the given preferences as well. However, avoid suggesting harmful treatment methods even the elder likes them.
- Avoid mixing facts from different areas.
3. Order of keys in the response must be "Thought", and "Technical Document".
4. Double-check compliance with all instructions.
</INSTRUCTIONS>
<QUERY>
{query}
</QUERY>

OUTPUT:
"""

def generate_suggestions(user_query,expert_llm,retriever,template=None):
    
    retrieved_documents = retrieve_documents(user_query,retriever)

    print(len(retrieved_documents))
    
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