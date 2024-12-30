from langchain_openai import OpenAIEmbeddings
from langchain_neo4j import Neo4jGraph
from langchain.text_splitter import CharacterTextSplitter
from certainty_estimator.predict_certainty import CertaintyEstimator
from dotenv import load_dotenv
from neo4j import GraphDatabase
import os

load_dotenv()
NEO4J_URI = os.getenv('NEO4J_URI')
NEO4J_USERNAME = os.getenv('NEO4J_USERNAME')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD')


driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD))

graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD)
text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
embeddings = OpenAIEmbeddings()
estimator = CertaintyEstimator('sentence-level')
# estimator = CertaintyEstimator('sentence-level',cuda=True)