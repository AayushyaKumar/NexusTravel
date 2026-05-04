export interface Destination {
  id: number;
  name: string;
  similarity_score: number;
  reason: string;
  cost: string;
  est_cost: number;
  climate: string;
  ratings: number;
  tags: string[];
  lat: number;
  lon: number;
}

export interface OptimizedRoute {
  id: number;
  name: string;
}

export interface MLResponse {
  parsed_preferences: {
    budget: string;
    climate: string | null;
    travel_type?: string;
    tags: string[];
  };
  clustering_evaluation: {
    inertia: number;
    silhouette_score: number | null;
  };
  recommendations: Destination[];
  similar_users_insight: string;
  optimized_travel_route: OptimizedRoute[];
}
