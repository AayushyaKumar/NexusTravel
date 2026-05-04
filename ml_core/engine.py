from .data import generate_mock_destinations, generate_mock_users
from .nlp import NLPParser
from .recommender import DestinationRecommender
from .clustering import UserClustering
from .routing import RouteOptimizer

class AITravelPlanner:
    """
    Main integrated engine for the AI Travel Planner.
    """
    def __init__(self):
        # Load datasets
        self.destinations_df = generate_mock_destinations()
        self.users_df = generate_mock_users()
        
        # Initialize ML components
        self.nlp = NLPParser()
        self.recommender = DestinationRecommender(self.destinations_df)
        self.clustering = UserClustering(self.users_df, n_clusters=4)
        self.routing = RouteOptimizer()
        
        # Train unsupervised models
        self.clustering.fit()
        
    def process_query(self, text_query: str):
        """
        End-to-end processing of a user's natural language query.
        """
        # 1. Parse natural language
        preferences = self.nlp.parse_query(text_query)
        
        # 2. Recommend Destinations
        recommendations = self.recommender.recommend(preferences, top_k=5)
        
        # 3. Cluster User and get insights
        cluster_id = self.clustering.get_user_cluster(preferences)
        cluster_stats = self.clustering.get_similar_users_stats(cluster_id)
        
        # 4. Route Optimization for the recommended trip
        optimized_route = self.routing.optimize_route(recommendations)
        
        return {
            "parsed_preferences": preferences,
            "clustering_evaluation": {
                "inertia": round(self.clustering.inertia, 2),
                "silhouette_score": round(self.clustering.silhouette_avg, 3) if self.clustering.silhouette_avg else None
            },
            "recommendations": recommendations,
            "similar_users_insight": f"Users like you (Cluster {cluster_id}) also enjoy {', '.join(cluster_stats['top_interests'])}.",
            "optimized_travel_route": optimized_route
        }

    def process_structured_query(self, preferences: dict):
        """
        Process a structured form input instead of natural language.
        Maps numeric budget to categorical and runs the same ML pipeline.
        """
        # Map numeric budget to categorical
        # If user passed "budget_max", map it
        if "budget_max" in preferences:
            budget_val = preferences["budget_max"]
            if budget_val < 50000:
                preferences["budget"] = "low"
            elif budget_val <= 150000:
                preferences["budget"] = "medium"
            else:
                preferences["budget"] = "high"
        
        # Recommendations
        recommendations = self.recommender.recommend(preferences, top_k=5)
        
        # Clustering
        cluster_id = self.clustering.get_user_cluster(preferences)
        cluster_stats = self.clustering.get_similar_users_stats(cluster_id)
        
        # Routing
        optimized_route = self.routing.optimize_route(recommendations)
        
        return {
            "parsed_preferences": preferences,
            "clustering_evaluation": {
                "inertia": round(self.clustering.inertia, 2),
                "silhouette_score": round(self.clustering.silhouette_avg, 3) if self.clustering.silhouette_avg else None
            },
            "recommendations": recommendations,
            "similar_users_insight": f"Users like you (Cluster {cluster_id}) also enjoy {', '.join(cluster_stats['top_interests'])}.",
            "optimized_travel_route": optimized_route
        }
