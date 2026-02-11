from langchain_neo4j import Neo4jGraph
from langchain_groq import ChatGroq
from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer
from config import NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD, GROQ_API_KEY

# Neo 4J support
graph = Neo4jGraph(
    url = NEO4J_URI,
    username = NEO4J_USERNAME,
    password = NEO4J_PASSWORD
)

llm = ChatGroq(
    groq_api_key = GROQ_API_KEY,
    model = "openai/gpt-oss-120b"
)

sample_text = """
Elon Reeve Musk (/ilɒn/ EE-lon; born June 28, 1971) is a businessman and entrepreneur known for his leadership of Tesla, SpaceX, Twitter, and xAI. Musk has been the wealthiest person in the world since 2025; as of February 2026, Forbes estimates his net worth to be around US$852 billion.
"""

# Convert text to proper document
documents = [Document(page_content = sample_text)]
print("Converted sample text into documents")

# Using LLM to convert the document into proper nodes and relationship graph
llm_transformer = LLMGraphTransformer(llm = llm)
graph_documents = llm_transformer.convert_to_graph_documents(documents)
print("Converted documents into graph using LLM")
print(graph_documents)

# View all the nodes created
print(graph_documents[0].nodes)

# View all the relationships created
print(graph_documents[0].relationships)