from langchain_community.document_loaders import PyPDFLoader

def exatract_pdf(filepath:str)->str:
    docs = PyPDFLoader(filepath)
    data= docs.load()


    texts=[]
    for document in data:
        texts.append(document.page_content)

    text="\n\n".join(texts)    

    return text

