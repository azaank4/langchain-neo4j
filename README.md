# LangChain Neo4j Knowledge Graph Builder

A Python project that integrates **LangChain** with **Neo4j** to transform unstructured text into knowledge graphs and enable natural language querying of graph databases using LLMs.

## Features

- **Text-to-Graph Transformation**: Convert unstructured text into structured knowledge graphs using `LLMGraphTransformer`
- **Neo4j Integration**: Seamless connection to Neo4j graph database with schema management
- **Natural Language Queries**: Use AI agents to generate and execute Cypher queries from plain English
- **CSV Data Loading**: Import structured data (e.g., movie datasets) into Neo4j with relationships
- **Groq LLM Support**: Leverage Groq's fast inference for graph operations

## Prerequisites

- Python 3.11 or higher
- Neo4j Database (Desktop or Cloud)
- [APOC Plugin](https://neo4j.com/docs/apoc/current/) installed in Neo4j (required for some operations)
- Groq API key ([Get one here](https://console.groq.com/))

## Installation

### Step 1: Create Virtual Environment

```bash
python -m venv .venv
```

Activate it:
- **Windows**: `.venv\Scripts\activate`
- **macOS/Linux**: `source .venv/bin/activate`

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Configure Environment

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Fill in your credentials in `.env`:

| Variable | Description |
|----------|-------------|
| `NEO4J_URI` | Neo4j connection URI (e.g., `bolt://localhost:7687`) |
| `NEO4J_USERNAME` | Neo4j username (default: `neo4j`) |
| `NEO4J_PASSWORD` | Neo4j password |
| `GROQ_API_KEY` | Your Groq API key |

## Usage

### Example 1: Text to Knowledge Graph (`test.py`)

Transform unstructured text into a Neo4j knowledge graph:

```python
from langchain_neo4j import Neo4jGraph
from langchain_groq import ChatGroq
from langchain_core.documents import Document
from langchain_experimental.graph_transformers import LLMGraphTransformer

# Initialize connections
graph = Neo4jGraph(url=NEO4J_URI, username=NEO4J_USERNAME, password=NEO4J_PASSWORD)
llm = ChatGroq(groq_api_key=GROQ_API_KEY, model="openai/gpt-oss-120b")

# Sample text
documents = [Document(page_content="Elon Musk is a businessman known for Tesla and SpaceX...")]

# Convert to graph
llm_transformer = LLMGraphTransformer(llm=llm)
graph_documents = llm_transformer.convert_to_graph_documents(documents)

# Store in Neo4j
graph.add_graph_documents(graph_documents)
```

Run it:
```bash
python test.py
```

### Example 2: Natural Language Querying (`rag.ipynb`)

Query your Neo4j database using natural language:

1. **Load Movie Dataset**:
   ```python
   movie_query = """
   LOAD CSV WITH HEADERS FROM 'https://raw.githubusercontent.com/tomasonjo/blog-datasets/main/movies/movies_small.csv' as row
   MERGE(m:Movie{id:row.movieId})
   SET m.released = date(row.released),
       m.title = row.title,
       m.imdbRating = toFloat(row.imdbRating)
   ...
   """
   graph.query(movie_query)
   ```

2. **Ask Questions in Natural Language**:
   ```python
   from langchain.agents import create_agent
   from langchain.tools import tool

   @tool
   def query_tool(cypher_query):
       """Execute a Cypher query on the Neo4j graph."""
       return str(graph.query(cypher_query))

   agent = create_agent(
       model=llm,
       tools=[query_tool],
       system_prompt="You are a helpful assistant that can query a knowledge graph."
   )

   result = agent.invoke({
       "messages": [{"role": "user", "content": "Which movie has the highest IMDB rating?"}]
   })
   ```

Open the notebook:
```bash
jupyter notebook rag.ipynb
```

## Project Structure

```
langchain-neo4j/
├── .env                 # Environment variables (gitignored)
├── .env.example         # Environment template
├── .gitignore          # Git ignore rules
├── config.py           # Configuration loader
├── test.py             # Text-to-graph example
├── rag.ipynb           # Natural language querying demo
└── README.md           # This file
```

| File | Purpose |
|------|---------|
| `config.py` | Loads environment variables for Neo4j and Groq credentials |
| `test.py` | Demonstrates converting text to knowledge graphs using LLMGraphTransformer |
| `rag.ipynb` | Jupyter notebook with movie dataset loading and agent-based querying |
| `.env.example` | Template for required environment variables |

## Technologies Used

- [LangChain](https://www.langchain.com/) - Framework for LLM applications
- [LangChain Neo4j](https://github.com/langchain-ai/langchain-neo4j) - Neo4j integration for LangChain
- [Neo4j](https://neo4j.com/) - Graph database
- [Groq](https://groq.com/) - Fast LLM inference API
- [LLMGraphTransformer](https://python.langchain.com/docs/integrations/graph_transformers/) - Convert text to graph structures

## Important Notes

1. **APOC Plugin**: If running Neo4j locally, ensure the [APOC plugin](https://neo4j.com/docs/apoc/current/) is installed and the database is restarted.

2. **Model Requirements**: The LLM used for graph transformation must support tool/function calling. This project uses `openai/gpt-oss-120b` via Groq.

3. **Graph Schema**: After loading data, run `graph.refresh_schema()` to update the schema for query generation.

4. **Deprecation Notice**: `GraphQAChain` has been deprecated; this project uses custom agent tools for querying instead.

## License

This project is open source and available under the [MIT License](LICENSE).

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
