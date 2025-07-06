# import RagPipeline
from rag_pipeline import TelcoRAGPipeline
from mock_data import TELCO_KNOWLEDGE_BASE

# Initialize the RAG pipeline
rag_pipeline = TelcoRAGPipeline(TELCO_KNOWLEDGE_BASE)

def get_grounded_response(query: str, top_k: int = 3) -> str:
    """
    Retrieve relevant snippets for the query using the RAG pipeline.
    Returns a formatted string with context, sources, and an indicator when knowledge is used
    """
    # Get the context snippets (formatted)
    context = rag_pipeline.get_context(query, top_k=top_k)
    # Retrieve detailed document info
    docs = rag_pipeline.retrieve(query, top_k=top_k)
    
    # Format sources info
    sources = "\n".join([f"Title: {doc['metadata']['title']}\nContent: {doc['content']}" for doc in docs])
    
    # Decide on indicator based on whether docs are retrieved
    if docs:
        indicator = "[Information retrieved from knowledge base]"
        # Incorporate retrieved info into response explicitly
        response_body = (
            f"{indicator}\n\nRelevant info:\n{context}\n\nSources:\n{sources}"
        )
    else:
        response_body = f"No relevant information found in knowledge base."
        
    # Return full response
    return f"Question: {query}\n{response_body}"
    
# Define three different questions
questions = [
    "How much does international roaming cost in the US?",
    "What is the difference between unlimited and basic plans?",
    "Are there any special offers for international travelers?"
]

# Use the function for each question and print
for q in questions:
    response = get_grounded_response(q)
    print(response)
    print("="*80)
