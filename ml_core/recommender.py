import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import OneHotEncoder

class DestinationRecommender:
    """
    Content-Based Recommendation System
    """
    def __init__(self, destinations_df: pd.DataFrame):
        self.destinations = destinations_df
        self.vectorizer = TfidfVectorizer()
        
        # Precompute destination features
        self._prepare_features()
        
    def _prepare_features(self):
        """
        Converts destination features into vectors.
        """
        # 1. Combine tags into a single text document for TF-IDF
        self.destinations['tags_text'] = self.destinations['tags'].apply(lambda x: " ".join(x))
        self.tag_matrix = self.vectorizer.fit_transform(self.destinations['tags_text']).toarray()
        
        # 2. One-hot encode categorical features (cost, climate)
        self.ohe = OneHotEncoder(handle_unknown='ignore')
        cat_features = self.destinations[['cost', 'climate', 'travel_type']]
        self.cat_matrix = self.ohe.fit_transform(cat_features).toarray()
        
        # 3. Combine TF-IDF and One-Hot matrices
        self.feature_matrix = np.hstack((self.tag_matrix, self.cat_matrix))
        
    def recommend(self, user_prefs: dict, top_k: int = 5):
        """
        Recommends destinations based on user preferences using Cosine Similarity.
        user_prefs format: {'budget': 'low', 'climate': 'warm', 'tags': ['beach', 'nightlife']}
        """
        # Format user tags for TF-IDF
        user_tags_text = " ".join(user_prefs.get('tags', []))
        user_tag_vec = self.vectorizer.transform([user_tags_text]).toarray()
        
        # Format user categorical features for OHE
        user_cat = pd.DataFrame([{
            'cost': user_prefs.get('budget', 'medium'),
            'climate': user_prefs.get('climate', 'moderate'), # Fallback if None
            'travel_type': user_prefs.get('travel_type', 'leisure')
        }])
        
        # Handle cases where user_prefs climate is None
        if user_cat['climate'][0] is None:
            user_cat['climate'] = 'moderate'
            
        user_cat_vec = self.ohe.transform(user_cat).toarray()
        
        # Combine user features
        user_feature_vec = np.hstack((user_tag_vec, user_cat_vec))
        
        # Calculate cosine similarity
        similarities = cosine_similarity(user_feature_vec, self.feature_matrix)[0]
        
        # Add similarities to dataframe
        results = self.destinations.copy()
        results['similarity_score'] = similarities
        
        # Strict budget filter
        if 'budget_max' in user_prefs:
            budget_max = user_prefs['budget_max']
            # Allow a tiny bit of wiggle room (e.g. +10%)
            budget_limit = budget_max * 1.1 
            budget_filtered = results[results['est_cost'] <= budget_limit]
            
            # If we actually found destinations within budget, use them. 
            # Otherwise, just return what we have (so it doesn't crash).
            if not budget_filtered.empty:
                results = budget_filtered
        
        # Sort and get top K
        results = results.sort_values(by='similarity_score', ascending=False).head(top_k)
        
        # Generate reasons
        recommendations = []
        for _, row in results.iterrows():
            matched_tags = set(user_prefs.get('tags', [])) & set(row['tags'])
            tag_reason = f"matches your interest in {', '.join(matched_tags)}" if matched_tags else "matches your general profile"
            
            reason = f"This destination has a {row['cost']} cost and {row['climate']} climate, and {tag_reason}."
            
            recommendations.append({
                "id": row['id'],
                "name": row['name'],
                "similarity_score": round(row['similarity_score'], 3),
                "reason": reason,
                "cost": row['cost'],
                "est_cost": int(row['est_cost']),
                "climate": row['climate'],
                "ratings": row['ratings'],
                "tags": row['tags'],
                "lat": row['lat'],
                "lon": row['lon']
            })
            
        return recommendations
