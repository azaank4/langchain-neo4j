Step 1:
create venv

Step 2:
pip install -r requirements.txt

Step 3:
Set up .gitignore file and create env file

Step 4:
config.py - Set up all the credentials

Step 5:
main.py
    - Install APOC plugin if running locally on Neo4J desktop and restart the database
    - Initialize Neo4J database and Groq LLM
    - Paste sample text, convert it into documents
    - Using LLMGraphTransformer, convert the provided documents into graph
    - Ensure the model being used for graph transformation supports tool call (openai/gpt-oss-120b)