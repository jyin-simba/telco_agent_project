from langchain.agents import Tool
from langchain.tools import BaseTool
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import json

# Import our models and data
from models import CustomerProfile, TelcoPlan, PlanRecommendation
from mock_data import MOCK_CUSTOMERS, TELCO_PLANS, TELCO_KNOWLEDGE_BASE
from rag_pipeline import TelcoRAGPipeline

# Initialize RAG pipeline
rag_pipeline = TelcoRAGPipeline(TELCO_KNOWLEDGE_BASE)

# Tool function implementations
def get_customer_profile_func(customer_id: str) -> str:
    """
    Retrieve customer profile and usage patterns.
    
    Args:
        customer_id: The customer's unique identifier
        
    Returns:
        JSON string of customer profile with usage history and preferences
    """
    try:
        customer = MOCK_CUSTOMERS.get(customer_id)
        if not customer:
            return json.dumps({"error": f"Customer {customer_id} not found"})
        
        return json.dumps(customer.model_dump(), indent=2)
    except Exception as e:
        return json.dumps({"error": f"Error retrieving customer profile: {str(e)}"})

def analyze_plan_suitability_func(input_str: str) -> str:
    """
    Analyze how well a specific plan fits a customer's usage pattern.
    
    Args:
        input_str: JSON string containing customer_id and plan_id
        
    Returns:
        JSON string with suitability analysis including score and reasoning
    """
    try:
        # Parse input
        input_data = json.loads(input_str)
        customer_id = input_data.get("customer_id")
        plan_id = input_data.get("plan_id")
        
        customer = MOCK_CUSTOMERS.get(customer_id)
        plan = next((p for p in TELCO_PLANS if p.plan_id == plan_id), None)
        
        if not customer or not plan:
            return json.dumps({"error": "Customer or plan not found"})
        
        usage = customer.usage_pattern
        
        # Calculate suitability score (0-100)
        score = 0
        reasoning_points = []
        
        # Data usage analysis
        if plan.data_allowance_gb == float('inf'):
            if usage.monthly_data_gb > 20:
                score += 30
                reasoning_points.append("Unlimited data perfect for heavy usage")
            else:
                score += 15
                reasoning_points.append("Unlimited data provides peace of mind")
        elif usage.monthly_data_gb <= plan.data_allowance_gb:
            score += 25
            reasoning_points.append(f"Data allowance ({plan.data_allowance_gb}GB) covers usage ({usage.monthly_data_gb}GB)")
        else:
            score -= 20
            reasoning_points.append(f"Insufficient data: {plan.data_allowance_gb}GB < {usage.monthly_data_gb}GB needed")
        
        # International usage
        if usage.international_usage and plan.international_included:
            score += 25
            reasoning_points.append("International calling included")
        elif usage.international_usage and not plan.international_included:
            score -= 15
            reasoning_points.append("No international calling - additional charges apply")
        
        # Budget analysis
        budget = float(customer.preferences.get("budget", "100"))
        if plan.monthly_cost <= budget:
            score += 20
            reasoning_points.append(f"Within budget: ${plan.monthly_cost} <= ${budget}")
        else:
            score -= 10
            reasoning_points.append(f"Over budget: ${plan.monthly_cost} > ${budget}")
        
        # Roaming analysis
        if usage.roaming_countries:
            avg_roaming_rate = sum(plan.roaming_rates.get(country, 0.20) for country in usage.roaming_countries) / len(usage.roaming_countries)
            if avg_roaming_rate < 0.05:
                score += 10
                reasoning_points.append("Excellent roaming rates")
            elif avg_roaming_rate < 0.10:
                score += 5
                reasoning_points.append("Good roaming rates")
        
        result = {
            "suitability_score": max(0, min(100, score)),
            "reasoning": "; ".join(reasoning_points),
            "monthly_cost": plan.monthly_cost,
            "potential_overage_cost": max(0, (usage.monthly_data_gb - plan.data_allowance_gb) * 10) if plan.data_allowance_gb != float('inf') else 0
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Error analyzing plan suitability: {str(e)}"})
    
def recommend_best_plans_func(input_str: str) -> str:
    """
    Recommend the best plans for a customer based on their usage pattern.
    
    Args:
        input_str: JSON string containing customer_id and optionally max_recommendations
        
    Returns:
        JSON string with list of recommended plans with suitability scores
    """
    try:
        input_data = json.loads(input_str) if input_str.strip().startswith('{') else {"customer_id": input_str.strip()}
        customer_id = input_data.get("customer_id")
        max_recommendations = input_data.get("max_recommendations", 3)
        
        customer = MOCK_CUSTOMERS.get(customer_id)
        if not customer:
            return json.dumps({"error": f"Customer {customer_id} not found"})
        
        recommendations = []
        
        for plan in TELCO_PLANS:
            analysis_input = json.dumps({"customer_id": customer_id, "plan_id": plan.plan_id})
            analysis_result = analyze_plan_suitability_func(analysis_input)
            analysis = json.loads(analysis_result)
            
            if "error" not in analysis:
                recommendations.append({
                    "plan": plan.model_dump(),
                    "analysis": analysis
                })
        
        # Sort by suitability score
        recommendations.sort(key=lambda x: x["analysis"]["suitability_score"], reverse=True)
        
        result = {
            "customer_id": customer_id,
            "recommendations": recommendations[:max_recommendations],
            "current_plan": customer.current_plan
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Error generating recommendations: {str(e)}"})

def search_telco_knowledge_func(query: str) -> str:
    """
    Search the telecommunications knowledge base for relevant information.
    
    Args:
        query: Search query about telco services, plans, or policies
        
    Returns:
        JSON string with relevant information from knowledge base with sources
    """
    try:
        context = rag_pipeline.get_context(query, top_k=3)
        retrieved_docs = rag_pipeline.retrieve(query, top_k=3)
        
        result = {
            "query": query,
            "context": context,
            "sources": [doc["metadata"] for doc in retrieved_docs],
            "rag_used": True,  # Indicator for response logs
            "num_sources": len(retrieved_docs)
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Error searching knowledge base: {str(e)}"})

def calculate_roaming_costs_func(input_str: str) -> str:
    """
    Calculate estimated roaming costs for international travel.
    
    Args:
        input_str: JSON string containing customer_id, destination_countries, and days
        
    Returns:
        JSON string with estimated roaming costs and recommendations
    """
    try:
        input_data = json.loads(input_str)
        customer_id = input_data.get("customer_id")
        destination_countries = input_data.get("destination_countries", [])
        days = input_data.get("days", 1)
        
        customer = MOCK_CUSTOMERS.get(customer_id)
        if not customer:
            return json.dumps({"error": f"Customer {customer_id} not found"})
        
        current_plan = next((p for p in TELCO_PLANS if p.plan_id == customer.current_plan), None)
        if not current_plan:
            return json.dumps({"error": "Current plan not found"})
        
        daily_usage = customer.usage_pattern.monthly_data_gb / 30  # Estimate daily usage
        
        roaming_costs = {}
        total_cost = 0
        
        for country in destination_countries:
            rate = current_plan.roaming_rates.get(country, 0.20)  # Default rate
            country_cost = daily_usage * rate * days
            roaming_costs[country] = {
                "daily_rate_per_gb": rate,
                "estimated_daily_usage_gb": daily_usage,
                "total_cost": country_cost
            }
            total_cost += country_cost
        
        # Check if traveler plan would be better
        traveler_plan = next((p for p in TELCO_PLANS if p.plan_id == "traveler_roaming"), None)
        recommendation = None
        
        if traveler_plan and total_cost > (traveler_plan.monthly_cost - current_plan.monthly_cost):
            recommendation = f"Consider switching to {traveler_plan.name} - would save approximately ${total_cost - (traveler_plan.monthly_cost - current_plan.monthly_cost):.2f}"
        
        result = {
            "destination_countries": destination_countries,
            "travel_days": days,
            "roaming_costs": roaming_costs,
            "total_estimated_cost": total_cost,
            "current_plan": current_plan.name,
            "recommendation": recommendation
        }
        
        return json.dumps(result, indent=2)
        
    except Exception as e:
        return json.dumps({"error": f"Error calculating roaming costs: {str(e)}"})

# Create LangChain Tool objects
get_customer_profile_tool = Tool(
    name="get_customer_profile",
    description="Retrieve customer profile and usage patterns. Input should be a customer ID string.",
    func=get_customer_profile_func
)

analyze_plan_suitability_tool = Tool(
    name="analyze_plan_suitability", 
    description="Analyze how well a specific plan fits a customer's usage pattern. Input should be a JSON string with 'customer_id' and 'plan_id' fields.",
    func=analyze_plan_suitability_func
)

recommend_best_plans_tool = Tool(
    name="recommend_best_plans",
    description="Recommend the best plans for a customer based on their usage pattern. Input should be a JSON string with 'customer_id' and optionally 'max_recommendations' fields, or just the customer_id as a string.",
    func=recommend_best_plans_func
)

search_telco_knowledge_tool = Tool(
    name="search_telco_knowledge",
    description="Search the telecommunications knowledge base for relevant information. Input should be a search query string about telco services, plans, or policies.",
    func=search_telco_knowledge_func
)

calculate_roaming_costs_tool = Tool(
    name="calculate_roaming_costs",
    description="Calculate estimated roaming costs for international travel. Input should be a JSON string with 'customer_id', 'destination_countries' (list), and 'days' (number) fields.",
    func=calculate_roaming_costs_func
)

# List of all tools for easy import
TELCO_TOOLS = [
    get_customer_profile_tool,
    analyze_plan_suitability_tool,
    recommend_best_plans_tool,
    search_telco_knowledge_tool,
    calculate_roaming_costs_tool
]

# Tool usage examples and testing functions
def test_tools():
    """Test function to verify all tools work correctly"""
    print("Testing Telco Tools...")
    
    # Test customer profile
    print("\n1. Testing get_customer_profile:")
    result = get_customer_profile_tool.run("CUST001")
    print(result)
    
    # Test plan analysis
    print("\n2. Testing analyze_plan_suitability:")
    result = analyze_plan_suitability_tool.run('{"customer_id": "CUST001", "plan_id": "premium_unlimited"}')
    print(result)
    
    # Test recommendations
    print("\n3. Testing recommend_best_plans:")
    result = recommend_best_plans_tool.run("CUST001")
    print(result)
    
    # Test knowledge search
    print("\n4. Testing search_telco_knowledge:")
    result = search_telco_knowledge_tool.run("roaming charges in Europe")
    print(result)
    
    # Test roaming costs
    print("\n5. Testing calculate_roaming_costs:")
    result = calculate_roaming_costs_tool.run('{"customer_id": "CUST001", "destination_countries": ["US", "UK"], "days": 7}')
    print(result)

# Alternative: Custom BaseTool implementations for more control
class CustomerProfileTool(BaseTool):
    name = "get_customer_profile"
    description = "Retrieve customer profile and usage patterns"
    
    def _run(self, customer_id: str) -> str:
        return get_customer_profile_func(customer_id)
    
    def _arun(self, customer_id: str) -> str:
        # Async version - for now just call sync version
        return self._run(customer_id)

class PlanRecommendationTool(BaseTool):
    name = "recommend_best_plans"
    description = "Recommend the best plans for a customer based on their usage pattern"
    
    def _run(self, input_str: str) -> str:
        return recommend_best_plans_func(input_str)
    
    def _arun(self, input_str: str) -> str:
        return self._run(input_str)

class TelcoKnowledgeTool(BaseTool):
    name = "search_telco_knowledge"
    description = "Search the telecommunications knowledge base for relevant information"
    
    def _run(self, query: str) -> str:
        return search_telco_knowledge_func(query)
    
    def _arun(self, query: str) -> str:
        return self._run(query)

# Alternative tool set using BaseTool
TELCO_BASE_TOOLS = [
    CustomerProfileTool(),
    PlanRecommendationTool(),
    TelcoKnowledgeTool()
]

if __name__ == "__main__":
    # Run tests when script is executed directly
    test_tools()
