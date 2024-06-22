
import os
from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI,GoogleGenerativeAI
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_community.retrievers import BM25Retriever

from langchain import LLMChain
from langchain.prompts import PromptTemplate
from langchain.schema.output_parser import StrOutputParser
from langchain_core.messages import HumanMessage

import torch

from qdrant_client import QdrantClient
from langchain_community.vectorstores import Qdrant

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

RETRIEVER_PROMPT_TEMPLATE = PromptTemplate(
    input_variables=["question"],
    template="""You are an AI language model assistant specializing in healthcare. Your task is to identify disease-related information, dietary plans, and treatment options from the given user question. You need to generate three different versions of the given user question to retrieve relevant documents from a vector database. By generating multiple perspectives on the user question, your goal is to help the user overcome some of the limitations of distance-based similarity search. Provide these alternative questions separated by newlines.

    Original question: {question}
    
    1. Alternative question focusing on disease-related information:
    2. Alternative question focusing on dietary plans:
    3. Alternative question focusing on treatment options:"""
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
            retriever=retriever, llm=expert_llm,prompt= RETRIEVER_PROMPT_TEMPLATE
        )
        
        return retriever_from_llm, expert_llm

    except Exception as ex:
        
        print("error in loading expert vector database: ",ex)
      

def concat_documents(documents):
    result = []
    for doc in documents:
        content = doc.page_content
        source = doc.metadata.get('source', 'No source provided')
        title = doc.metadata.get('title', 'No title provided')
        result.append(f"Document Title: {title}, Source: {source}\nContent:\n{content}\n")
    
    return "\n".join(result)

  

def retrieve_documents(user_query,retriever, k):
    retrieved_docs = retriever.invoke(user_query)
    # retrieved_docs = vdb.similarity_search_with_score(user_query, k=3,)
        
    bm25_retriever = BM25Retriever.from_documents(retrieved_docs)
    bm25_retriever.k =  k 
    bm25_retrieved_docs = bm25_retriever.invoke(user_query)
    similar_docs = bm25_retrieved_docs
    document_text = [doc.page_content for doc in similar_docs]
    document_text = concat_documents(similar_docs)
    
    return document_text

PROMPT_TEMPLATE = """
You are a medical expert for suggesting treatment methods based on the provided documents to identified medical requirements in the query to the caregiver.
Your mission is to provide both the treatments we should provide and we should avoid for the identified medical requirements.
You should organize your response in a professional, objective tone. Provide your thought process to explain how you reasoned to provide the response.

Steps:
1. Read and analyze the given query comprehensively and identify the medical requirements, including care needs if there are any, like dementia, arthritis, Alzheimer's, diabetes, etc.
2. Read and understand the information in documents thoroughly for the identified medical requirements and care needs.
3. ONLY IF REQUIRED, use all information provided in the document to think about how to provide the correct medical treatments to be performed by the caregiver. Here please consider the proper medical treatments which the elder might like to do using the provided query.
4. If the information in the document overlaps or has duplicate details, select the most detailed and comprehensive information that is most similar to the provided query details. However, if the details provided in the query for the elder seem fine, meaning the elder seems healthy, you must not provide unnecessary information (care needs) or treatments as suggestions.
5. Remember to provide both treatment methods: what we should do and what we should not do. Again, do not provide any unnecessary treatments to the elder if you consider the elder is doing fine from the provided details in the query.

Now it's your turn!

<DOCUMENT>
{context}
</DOCUMENT>
<INSTRUCTIONS>
Your response should include a 2-step cohesive answer with the following keys:
1. "Thought" key: Explain how you would use the information in the document to partially or completely answer the query. Your thought process includes why you suggest the treatment methods based on the preference of the elder and thoroughly referring to the information in the document. However, you should not provide treatment methods that are not related to the document for the analyzed condition for the provided query and any treatment, activity, or food type which could cause any harm to the elder even if the elder likes to do them.
2. "Technical Document":
    - Present each treatment method accurately without adding new information but explain in detail why you need to give this treatment (food, medicine, activity, tools, etc.) based on the elder's conditions.
    - Treatment methods might include possible nutrients (meal), physical exercises, mental exercises, proper caregiver tools, etc. While suggesting the treatment methods, consider the given preferences as well. However, avoid suggesting harmful treatment methods even if the elder likes them.
    - Avoid mixing facts from different areas.
3. Order of keys in the response must be "Thought" and "Technical Document".
4. Double-check compliance with all instructions.
</INSTRUCTIONS>
<QUERY>
{query}
</QUERY>

OUTPUT:
"""



# PROMPT_TEMPLATE = """
# You are a medical expert for suggesting treatment methods based on the provided documents to identified medical requirements in the query to the caregiver.
# Your mission is to provide both the treatments we should provide and we should avoid for the identified medical requirements.
# You should organize your response in a professional, objective tone. Provide your thought
# process to explain how you reasoned to provide the response.


# Steps:
# 1. Read and Analyze the given query comprehensively and identify the medical requirements including care needs if there are any like dimentia, arthuritis, alzhemizer, diabetes, etc.
# 1. Read and understand the information in documents thoroughly for the identified medical requirements and care needs.
# 2. ONLY IF REQUIRED , use all information provided in the document to think about how to provide the correct medical treatments to perform by the caregiver. Here please consider the proper medical treatments which the elder might like to do using the provided query.
# 3. If the information in the document are overlapping or have duplicate details, select information which are most detailed and comprehensive which most similar to provided query details. However, if the details provided in the query for the elder seems fine means the elder seems healthy, you must not provide \
# unnecessary information (care needs) or treatments as suggestions.
# 4. Remember to provide both treatments methods what we should do and what we should not do. Again, do not provide any unnecessary treatments to the elder if you can consider the elder is doing fine from the provided details in the query.

# Now it's your turn!

# <DOCUMENT>
# {context}s
# </DOCUMENT>
# <INSTRUCTIONS>
# Your response should include a 2-step cohesive answer with following keys:
# 1. "Thought" key: Explain how you would use the information in the document to partially or
# completely answer the query. Your thought process includes that why do you suggest the treatment methods based on the preference of the elder and thoughroghly referring \
# to the information in the document. However, you should not provide the treatment methods which are not related to the document for the analysed condition for the provided query and any treatment, activity \
#     or food type which cause any harm to the elder even if elder likes to do them.
# 2. "Technical Document":
# - Present each treatment method accurately without adding new information but explain in detail why you need to give this treatment (food, medicine, activity, tools, etc.) based on the elders conditions.
# - Treatment method might include the possible nutrients (meal), physical exercises, mental exercises, proper care giver tools, etc. While suggesting the treatment methods, consider the given preferences as well. However, avoid suggesting harmful treatment methods even the elder likes them.
# - Avoid mixing facts from different areas.
# 3. Order of keys in the response must be "Thought", and "Technical Document".
# 4. Double-check compliance with all instructions.
# </INSTRUCTIONS>
# <QUERY>
# {query}
# </QUERY>

# OUTPUT:
# """

def expand_query(expert_llm, query):
    prompt_template = """
        You are an AI assistant. Your task is to enhance the user query to improve the vector database search.

        <INSTRUCTIONS>
        Follow these steps:
        1. Identify disease, dietary plan, and treatment-related topics only from the user query.
        2. Divide the topics into multiple meaningful sub-contents.
        3. Enhance each sub-content to improve clarity and precision.
        4. Ensure each sub-content is a concise and clear paragraph.
        5. Do not add any unwanted information.
        6. Rephrase or restructure each sub-content for better searchability without altering the original meaning.
        </INSTRUCTIONS>

        <QUERY>
        {query}
        </QUERY>

        Output should be a string and differentiate using "*".
        Example:
        sub-content 1 * sub-content 2 * ...

        OUTPUT:
        """


    user_query = prompt_template.format(query=query)
    response = expert_llm.invoke(user_query)
    return response
    

def generate_suggestions(user_query,expert_llm,retriever,template=None):
    # try:
    #     res_list = [content for content in expand_query(expert_llm, user_query).split("*") if content]
    #     print(f"Expand query: {res_list}")
    #     retrieved_documents = "\n".join(sum((retrieve_documents(data, retriever, 3) for data in res_list), []))
        
    # except:
    retrieved_documents = retrieve_documents(user_query,retriever,10)
    print("-------"*15)
    print(f"User Query: \n {user_query}")
    print("-------"*15)
    print(f"Documents: \n{retrieved_documents}")
    print("-------"*15)
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