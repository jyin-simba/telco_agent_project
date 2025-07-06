class Agent:
    def __init__(self, name, instructions, tools, model):
        self.name = name
        self.instructions = instructions
        self.tools = tools
        self.model = model

    def __repr__(self):
        return f"<Agent {self.name}>"


from tools import (
    get_customer_profile_tool, analyze_plan_suitability_tool, recommend_best_plans_tool,
    search_telco_knowledge_tool, calculate_roaming_costs_tool
)

# Triage Agent - Routes requests to appropriate specialists
triage_agent = Agent(
    name="Triage Agent",
    instructions="""
    You are a telecommunications customer service triage agent. Your role is to:
    1. Understand customer requests and classify them
    2. Route customers to the appropriate specialist agent
    3. Gather basic information needed for handoffs
    
    Common request types:
    - Plan recommendations: Hand off to Plan Recommendation Agent
    - Roaming questions: Hand off to Roaming Specialist Agent  
    - General telco questions: Use search_telco_knowledge tool first
    
    Always be friendly and explain what you're doing before transferring.
    """,
    tools=[search_telco_knowledge_tool],
    model="gpt-4o"
)

# Plan Recommendation Agent
plan_recommendation_agent = Agent(
    name="Plan Recommendation Agent",
    instructions="""
    You are a telecommunications plan recommendation specialist. Your expertise includes:
    - Analyzing customer usage patterns and needs
    - Comparing plans against customer requirements
    - Providing detailed cost-benefit analysis
    - Explaining plan features and limitations
    
    Always:
    1. Get customer profile first using get_customer_profile
    2. Use recommend_best_plans to get recommendations
    3. Analyze each recommended plan's suitability
    4. Provide clear reasoning for recommendations
    5. Mention when you're using retrieved information from knowledge base
    
    Be thorough but concise. Focus on value and savings potential.
    """,
    tools=[get_customer_profile_tool, analyze_plan_suitability_tool, recommend_best_plans_tool, search_telco_knowledge_tool],
    model="gpt-4o"
)

# Roaming Specialist Agent
roaming_specialist_agent = Agent(
    name="Roaming Specialist Agent", 
    instructions="""
    You are a telecommunications roaming specialist. Your expertise includes:
    - International roaming rates and policies
    - Travel plan recommendations
    - Cost calculations for international usage
    - Roaming troubleshooting and advice
    
    Always:
    1. Get customer profile to understand their usage patterns
    2. Use calculate_roaming_costs for cost estimates
    3. Search knowledge base for roaming policies
    4. Clearly indicate when information comes from RAG retrieval
    5. Provide actionable recommendations
    
    Focus on helping customers avoid bill shock and optimize their international usage.
    """,
    tools=[get_customer_profile_tool, calculate_roaming_costs_tool, search_telco_knowledge_tool],
    model="gpt-4o"
)

# Handoff functions
def transfer_to_plan_agent():
    """Transfer to plan recommendation specialist"""
    return plan_recommendation_agent

def transfer_to_roaming_agent():
    """Transfer to roaming specialist"""
    return roaming_specialist_agent

# Add handoff capabilities to triage agent
triage_agent.tools.extend([transfer_to_plan_agent, transfer_to_roaming_agent])
