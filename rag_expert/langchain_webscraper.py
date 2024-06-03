from langchain_community.document_transformers import Html2TextTransformer
from langchain_community.document_loaders import AsyncHtmlLoader


from langchain.docstore.document import Document



def retrieve_documents(urls,save_dir=None,character_splitter = None):
    loader = AsyncHtmlLoader(urls)
    
    if character_splitter:
        docs = loader.load_and_split(text_splitter=character_splitter)
    else:
        docs = loader.load()

    html2text = Html2TextTransformer()
    docs_transformed = html2text.transform_documents(docs)
    docs_transformed = [Document(page_content=doc.page_content,metadata=doc.metadata) for doc in docs_transformed]
    print(len(docs_transformed))
    # print(docs_transformed[0])
    print(type(docs_transformed[0]))
    

    # print(docs_transformed[1])
    
    if save_dir:
        for doc in docs_transformed:
            
            source_url = doc.metadata['source']
            title = doc.metadata['title'].replace(" ","_")
            page_content = doc.page_content + f"\n\nOriginal source URL: {source_url}"
            
            txt_file_save_path = save_dir + f"/{title}.txt"
            
            with open(txt_file_save_path,'w') as fl:
                fl.write(page_content)

    return docs_transformed

if __name__=="__main__":
    urls = ["https://nurseslabs.com/geriatric-nursing-care-plans/","https://www.betterhealth.vic.gov.au/health/healthyliving/Nutrition-needs-when-youre-over-65","https://www.assistinghands-il-wi.com/blog/foods-good-for-arthritis/"]
    
    
    retrieve_documents(urls)