# mock_data.py
from models import TelcoPlan, CustomerProfile, UsagePattern

# Mock telco plans database
TELCO_PLANS = [
    TelcoPlan(
        plan_id="basic_mobile",
        name="Basic Mobile Plan",
        monthly_cost=25.0,
        data_allowance_gb=5.0,
        minutes_included=500,
        sms_included=1000,
        international_included=False,
        roaming_rates={"EU": 0.05, "US": 0.10, "ASIA": 0.15},
        features=["4G Network", "Voicemail"]
    ),
    TelcoPlan(
        plan_id="premium_unlimited",
        name="Premium Unlimited",
        monthly_cost=65.0,
        data_allowance_gb=float('inf'),
        minutes_included=99999,
        sms_included=99999,
        international_included=True,
        roaming_rates={"EU": 0.02, "US": 0.05, "ASIA": 0.08},
        features=["5G Network", "International Calls", "Premium Support", "Device Insurance"]
    ),
    TelcoPlan(
        plan_id="traveler_roaming",
        name="Global Traveler",
        monthly_cost=45.0,
        data_allowance_gb=15.0,
        minutes_included=1000,
        sms_included=2000,
        international_included=True,
        roaming_rates={"EU": 0.01, "US": 0.03, "ASIA": 0.05},
        features=["Global Roaming", "Travel Insurance", "Multi-country Data"]
    )
]

# Mock customer database
MOCK_CUSTOMERS = {
    "CUST001": CustomerProfile(
        customer_id="CUST001",
        name="John Doe",
        current_plan="basic_mobile",
        usage_pattern=UsagePattern(
            monthly_data_gb=12.5,
            monthly_minutes=800,
            monthly_sms=150,
            international_usage=True,
            roaming_countries=["US", "UK"],
            avg_monthly_bill=35.0
        ),
        preferences={"budget": "50", "priority": "data"}
    )
}

# Knowledge base documents for RAG
TELCO_KNOWLEDGE_BASE = [
    {
        "title": "Roaming Charges Guide",
        "content": "When traveling internationally, roaming charges apply based on destination country. EU roaming is typically cheaper due to regulations. Always check roaming rates before travel and consider roaming packages.",
        "category": "roaming"
    },
    {
        "title": "Data Plan Comparison",
        "content": "Unlimited plans offer best value for heavy users (>20GB/month). Basic plans suitable for light users (<5GB/month). Consider 5G availability in your area when choosing plans.",
        "category": "plans"
    },
    {
        "title": "International Calling",
        "content": "International calling rates vary by destination. Premium plans include international minutes. VoIP alternatives like WhatsApp calling can reduce costs.",
        "category": "international"
    }
]
