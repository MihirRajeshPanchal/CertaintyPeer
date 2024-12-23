import json
from langchain_community.document_loaders import JSONLoader
from langchain_neo4j import Neo4jVector
from certaintypeer.constants.certaintypeer import text_splitter, embeddings, NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD
from langchain.schema import Document

def create_embeddings(file_path, query):
    jq_schema = ".reviews[] | {review: .review, rating: .rating, confidence: .confidence}"
    
    loader = JSONLoader(file_path, jq_schema=jq_schema, text_content=False)
    raw_documents = loader.load()
    
    documents = [
        Document(
            page_content=str(doc.page_content),  
            metadata=doc.metadata
        ) for doc in raw_documents
    ]
    
    docs = text_splitter.split_documents(documents)
    
    serializable_docs = [
        {
            "page_content": str(doc.page_content),
            "metadata": dict(doc.metadata)
        } for doc in docs
    ]
    
    with open("split_documents.json", "w") as f:
        json.dump(serializable_docs, f, indent=4)
    
    db = Neo4jVector.from_documents(
        docs, 
        embeddings, 
        url=NEO4J_URI, 
        username=NEO4J_USERNAME, 
        password=NEO4J_PASSWORD
    )
    
    docs_with_score = db.similarity_search_with_score(query, k=2)
    return docs_with_score