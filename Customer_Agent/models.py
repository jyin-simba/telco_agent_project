from pydantic import BaseModel
from typing import List, Optional, Dict
from enum import Enum

class UsagePattern(BaseModel):
    monthly_data_gb: float
    monthly_minutes: int
    monthly_sms: int
    international_usage: bool
    roaming_countries: List[str]
    avg_monthly_bill: float

class CustomerProfile(BaseModel):
    customer_id: str
    name: str
    current_plan: str
    usage_pattern: UsagePattern
    preferences: Dict[str, str]  # budget, features, etc.

class TelcoPlan(BaseModel):
    plan_id: str
    name: str
    monthly_cost: float
    data_allowance_gb: float
    minutes_included: int
    sms_included: int
    international_included: bool
    roaming_rates: Dict[str, float]
    features: List[str]

class PlanRecommendation(BaseModel):
    recommended_plan: TelcoPlan
    savings_potential: float
    suitability_score: float
    reasoning: str
