from ml_core.engine import AITravelPlanner
import json

def main():
    print("Initializing AI Travel Planner ML Engine...")
    planner = AITravelPlanner()
    
    print("\n" + "="*50)
    print("Test Case 1: Beach and Nightlife Vacation")
    query1 = "I want a cheap beach vacation with good nightlife"
    print(f"Query: '{query1}'")
    
    result1 = planner.process_query(query1)
    print("\nResult:")
    print(json.dumps(result1, indent=2))
    
    print("\n" + "="*50)
    print("Test Case 2: Cultural European Trip")
    query2 = "Looking for a moderate climate to explore history and culture"
    print(f"Query: '{query2}'")
    
    result2 = planner.process_query(query2)
    print("\nResult:")
    print(json.dumps(result2, indent=2))

if __name__ == "__main__":
    main()
