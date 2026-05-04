import re

class NLPParser:
    """
    Basic NLP Processing for parsing user text queries into structured preferences.
    """
    def __init__(self):
        # Predefined categories for simple keyword mapping
        self.keywords = {
            "budget": {
                "low": ["cheap", "budget", "affordable", "inexpensive", "low-cost"],
                "high": ["luxury", "expensive", "premium", "lavish", "high-end"],
                "medium": ["moderate", "reasonable", "standard"]
            },
            "climate": {
                "warm": ["warm", "sunny", "hot", "tropical"],
                "cold": ["cold", "snow", "chilly", "winter"],
                "moderate": ["moderate", "mild", "spring", "autumn", "fall"]
            },
            "tags": {
                "beach": ["beach", "ocean", "sea", "sand", "coast"],
                "nightlife": ["nightlife", "party", "club", "bars", "dancing"],
                "nature": ["nature", "mountains", "forest", "hiking", "scenery", "wildlife"],
                "history": ["history", "ruins", "museums", "historical", "ancient"],
                "cultural": ["culture", "tradition", "art", "temples"],
                "adventure": ["adventure", "trekking", "extreme", "sports", "action"],
                "food": ["food", "culinary", "dining", "restaurants", "eating"],
                "leisure": ["leisure", "relax", "spa", "chill", "peaceful"]
            }
        }

    def parse_query(self, text: str):
        """
        Parses a natural language query and extracts structured parameters.
        Example: "I want a cheap beach vacation with nightlife"
        """
        text = text.lower()
        extracted = {
            "budget": "medium", # Default
            "climate": None,
            "tags": []
        }
        
        # Extract Budget
        for level, words in self.keywords["budget"].items():
            if any(re.search(rf"\b{word}\b", text) for word in words):
                extracted["budget"] = level
                break
                
        # Extract Climate
        for level, words in self.keywords["climate"].items():
            if any(re.search(rf"\b{word}\b", text) for word in words):
                extracted["climate"] = level
                break
                
        # Extract Tags
        for tag, words in self.keywords["tags"].items():
            if any(re.search(rf"\b{word}\b", text) for word in words):
                extracted["tags"].append(tag)
                
        return extracted
