import os
from dotenv import load_dotenv
from agents import triage_agent
import json

def run_demo_loop(agent, stream=False):
    print(f"Starting session with {agent.name}")
    print("Type 'exit' to quit.")
    while True:
        user_input = input("User: ")
        if user_input.lower() == 'exit':
            print("Ending session. Goodbye!")
            break
        # Simulate agent response
        response = simulate_agent_response(user_input, agent)
        print(f"{agent.name}: {response}")

def simulate_agent_response(user_input, agent):
    # Detect intent based on keywords
    if "roam" in user_input.lower():
        # Example: call the roaming costs tool with dummy data
        user_data = json.dumps({"customer_id": "CUST001", "destination_countries": ["US", "UK"], "days": 7})
        result = agent.tools[2]._run(user_data)  # assuming 3rd tool is calculate_roaming_costs
        return f"Here are your roaming costs:\n{result}"

    elif "plan" in user_input.lower():
        # Call plan recommendation tool
        result = agent.tools[3]._run("CUST001")
        return f"Plan recommendations:\n{result}"

    elif "knowledge" in user_input.lower() or "question" in user_input.lower():
        # Call the knowledge base search
        result = agent.tools[4]._run(user_input)
        return f"Here's what I found:\n{result}"

    else:
        return "I'm here to answer your questions about plans, roaming, or services!"

# Load environment variables
load_dotenv()

def main():
    """Run the telecommunications customer service agent"""
    
    print("Telecommunications Customer Service Agent")
    print("=" * 50)
    print("I can help you with:")
    print("• Plan recommendations based on your usage")
    print("• Roaming costs and international travel advice") 
    print("• General telecommunications questions")
    print("• Billing and plan comparisons")
    print("\nExample: 'I need a new plan recommendation' or 'What will roaming cost in Europe?'")
    print("=" * 50)
    
    # Run the agent loop
    run_demo_loop(triage_agent, stream=True)

if __name__ == "__main__":
    main()
