import pandas as pd
import numpy as np

def generate_mock_destinations():
    """Generates a mock dataset of destinations."""
    destinations = [
        {"id": 1, "name": "Bali, Indonesia", "cost": "medium", "est_cost": 100000, "climate": "warm", "travel_type": "leisure", "ratings": 4.8, "tags": ["beach", "nature", "nightlife", "leisure"], "lat": -8.4095, "lon": 115.1889},
        {"id": 2, "name": "Paris, France", "cost": "high", "est_cost": 280000, "climate": "moderate", "travel_type": "family", "ratings": 4.7, "tags": ["cultural", "history", "food", "shopping"], "lat": 48.8566, "lon": 2.3522},
        {"id": 3, "name": "Reykjavik, Iceland", "cost": "high", "est_cost": 320000, "climate": "cold", "travel_type": "adventure", "ratings": 4.9, "tags": ["nature", "mountains", "adventure"], "lat": 64.1466, "lon": -21.9426},
        {"id": 4, "name": "Bangkok, Thailand", "cost": "low", "est_cost": 50000, "climate": "warm", "travel_type": "solo", "ratings": 4.6, "tags": ["nightlife", "food", "shopping"], "lat": 13.7563, "lon": 100.5018},
        {"id": 5, "name": "Kyoto, Japan", "cost": "medium", "est_cost": 150000, "climate": "moderate", "travel_type": "solo", "ratings": 4.9, "tags": ["cultural", "history", "nature"], "lat": 35.0116, "lon": 135.7681},
        {"id": 6, "name": "Machu Picchu, Peru", "cost": "medium", "est_cost": 120000, "climate": "moderate", "travel_type": "adventure", "ratings": 4.8, "tags": ["history", "adventure", "mountains"], "lat": -13.1631, "lon": -72.5450},
        {"id": 7, "name": "Goa, India", "cost": "low", "est_cost": 25000, "climate": "warm", "travel_type": "leisure", "ratings": 4.3, "tags": ["beach", "nightlife", "leisure"], "lat": 15.2993, "lon": 74.1240},
        {"id": 8, "name": "Swiss Alps", "cost": "high", "est_cost": 360000, "climate": "cold", "travel_type": "family", "ratings": 4.8, "tags": ["nature", "mountains", "adventure"], "lat": 46.5601, "lon": 7.9734},
        {"id": 9, "name": "Rome, Italy", "cost": "medium", "est_cost": 160000, "climate": "moderate", "travel_type": "family", "ratings": 4.7, "tags": ["history", "food", "cultural"], "lat": 41.9028, "lon": 12.4964},
        {"id": 10, "name": "Cancun, Mexico", "cost": "medium", "est_cost": 110000, "climate": "warm", "travel_type": "leisure", "ratings": 4.5, "tags": ["beach", "nightlife", "leisure"], "lat": 21.1619, "lon": -86.8515},
        {"id": 11, "name": "Kerala, India", "cost": "medium", "est_cost": 45000, "climate": "warm", "travel_type": "family", "ratings": 4.8, "tags": ["nature", "beach", "food"], "lat": 10.8505, "lon": 76.2711},
        {"id": 12, "name": "Manali, India", "cost": "low", "est_cost": 15000, "climate": "cold", "travel_type": "adventure", "ratings": 4.6, "tags": ["mountains", "nature", "adventure"], "lat": 32.2396, "lon": 77.1887},
        {"id": 13, "name": "Jaipur, India", "cost": "medium", "est_cost": 30000, "climate": "warm", "travel_type": "leisure", "ratings": 4.7, "tags": ["history", "cultural", "shopping"], "lat": 26.9124, "lon": 75.7873},
        {"id": 14, "name": "Andaman, India", "cost": "high", "est_cost": 85000, "climate": "warm", "travel_type": "leisure", "ratings": 4.9, "tags": ["beach", "nature", "adventure"], "lat": 11.7401, "lon": 92.6586},
        {"id": 15, "name": "Rishikesh, India", "cost": "low", "est_cost": 8000, "climate": "moderate", "travel_type": "adventure", "ratings": 4.8, "tags": ["mountains", "adventure", "nature", "history"], "lat": 30.0869, "lon": 78.2676},
        {"id": 16, "name": "Gokarna, India", "cost": "low", "est_cost": 9000, "climate": "warm", "travel_type": "solo", "ratings": 4.6, "tags": ["beach", "nature", "nightlife"], "lat": 14.5500, "lon": 74.3188},
        {"id": 17, "name": "Pushkar, India", "cost": "low", "est_cost": 7000, "climate": "warm", "travel_type": "solo", "ratings": 4.5, "tags": ["history", "cultural", "shopping"], "lat": 26.4883, "lon": 74.5509},
        {"id": 18, "name": "Varanasi, India", "cost": "low", "est_cost": 6000, "climate": "moderate", "travel_type": "family", "ratings": 4.7, "tags": ["history", "cultural", "nature"], "lat": 25.3176, "lon": 82.9739},
    ]
    return pd.DataFrame(destinations)

def generate_mock_users():
    """Generates a mock dataset of historical users for clustering."""
    np.random.seed(42)
    users = []
    for i in range(100):
        budget_pref = np.random.choice(["low", "medium", "high"])
        climate_pref = np.random.choice(["cold", "warm", "moderate"])
        travel_type_pref = np.random.choice(["adventure", "leisure", "solo", "family"])
        tags = np.random.choice(["beach", "nature", "nightlife", "history", "cultural", "adventure", "food", "leisure"], size=3, replace=False)
        users.append({
            "user_id": i + 1,
            "pref_budget": budget_pref,
            "pref_climate": climate_pref,
            "pref_travel_type": travel_type_pref,
            "pref_tags": list(tags)
        })
    return pd.DataFrame(users)
