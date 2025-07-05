# Telecommunication Customer Agent Solution
The purpose of creating the Customer Agent is to provide a Telco Products/Roaming plan recommendation engine. 
This repository contains the Builing of Customer Agent & Tool, Implementation of Retrieval-Augmented Generation(RAG) and Integration Strategy & Approach.

## Business Problem and Solution
This Telco Products/Roaming Plan Recommendation Engine targets to do recommendations based on the following analysis:
1. 	Analyzing customer usage patterns
2.	Comparing available plans against customer needs
3.	Providing personalized recommendations with cost analysis
4.	Handling roaming plan queries for international travelers

## Solution Architecture
The Recommendation Engine is built with a multi-agent system and the system consists with the following parts:
1.	Triage Agent: Routes customer requests to appropriate specialists
2.	Plan Recommendation Agent: Analyzes needs and recommends optimal plans
3.	Roaming Specialist Agent: Handles international roaming queries
4.	Customer Profile Tool: Retrieves customer data and usage history
5.	Plan Comparison Tool: Compares plans against customer requirements
6.	RAG Pipeline: Provides context from telco knowledge base

## Implementation Steps

### Environment Setup
First step is to create and activate the virtual environment
```bash
python -m venv telco_agent_env
source telco_agent_env/bin/activate
```
### Install Dependencies
Then install required packages
```bash
pip install openai-agents
pip install fastapi uvicorn
pip install sentence-transformers
pip install faiss-cpu
pip install pandas numpy
pip install langchain langchain-community
pip install chromadb
pip install python-dotenv
pip install pydantic
```
### Environment Configuration
Next step is to create a .env file which contains:
```YAML
OPENAI_API_KEY= your-openai-api-key
TELCO_DB_PATH=/PATH/TO/telco_agent_env/data/telco_knowledge_base
VECTOR_DB_PATH=/PATH/TO/telco_agent_env/data/vector_store
```
You can create your openai secrete key and replace 'your-openai-api-key' with it.
### Customer Profile and Data Models
Based on the business problem, I created folder ``Customer Agent`` which includes the following scripts:

``models.py``: It defines data models for representing customer profiles, usage patterns, plans, and recommendations in a telecommunications context, facilitating structured handling and analysis of user and plan data.
``mock_data.py``: It creates mock data for telecom plans, customer profiles, usage patterns, and knowledge base documents to facilitate testing and development of telecom-related applications.
### RAG Pipeline Implementation
A Retrieval-Augmented Generation (RAG)  pipeline is used to retrieve relevant factual information from knowledge base to ground responses. I created folder ``RAG Pipeline`` which includes the following scripts:
``RAG_pipeline``: It defines RAG pipeline that encodes knowledge base documents into vectors, builds a FAISS similarity index for fast retrieval, and provides methods to retrieve and format relevant documents based on user queries.
``RAG_implement``: It uses my mocked knowledge base to ground the agent's reposnese.





