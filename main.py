from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Union
from ml_core.engine import AITravelPlanner

app = FastAPI(title="AI Travel Planner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

planner = AITravelPlanner()

class StructuredQuery(BaseModel):
    budgetMin: int
    budgetMax: int
    duration: int
    travelType: str
    climate: str
    interests: List[str]

class QueryRequest(BaseModel):
    isStructured: bool
    data: Union[str, StructuredQuery]

@app.post("/api/recommend")
async def recommend(request: QueryRequest):
    if request.isStructured:
        # It's a structured query
        req_data = request.data
        preferences = {
            "budget_max": req_data.budgetMax,
            "budget_min": req_data.budgetMin,
            "duration": req_data.duration,
            "travel_type": req_data.travelType.lower(),
            "climate": req_data.climate.lower(),
            "tags": [tag.lower() for tag in req_data.interests]
        }
        
        # We also need to filter the dataframe in recommender before finding similarity, 
        # so it ONLY returns places within budget.
        # But engine currently only recommends from all. We will modify engine.py to handle filtering.
        result = planner.process_structured_query(preferences)
        return result
    else:
        # Natural language query
        result = planner.process_query(request.data)
        return result
