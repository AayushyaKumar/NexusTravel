import pandas as pd
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MultiLabelBinarizer, OneHotEncoder
import numpy as np

class UserClustering:
    """
    User Clustering using K-Means to find similar users.
    """
    def __init__(self, users_df: pd.DataFrame, n_clusters: int = 4):
        self.users = users_df
        self.n_clusters = n_clusters
        self.kmeans = KMeans(n_clusters=self.n_clusters, random_state=42, n_init=10)
        
        # Transformers
        self.mlb = MultiLabelBinarizer()
        self.ohe = OneHotEncoder(handle_unknown='ignore')
        
        self.cluster_labels = None
        self.silhouette_avg = None
        self.inertia = None
        
    def fit(self):
        """Preprocesses user data and fits K-Means."""
        # Process tags
        tag_matrix = self.mlb.fit_transform(self.users['pref_tags'])
        
        # Process categorical features
        cat_matrix = self.ohe.fit_transform(self.users[['pref_budget', 'pref_climate', 'pref_travel_type']]).toarray()
        
        # Combine
        self.feature_matrix = np.hstack((tag_matrix, cat_matrix))
        
        # Fit KMeans
        self.cluster_labels = self.kmeans.fit_predict(self.feature_matrix)
        self.users['cluster'] = self.cluster_labels
        
        # Evaluation
        self.inertia = self.kmeans.inertia_
        # Silhouette score requires at least 2 clusters
        if self.n_clusters > 1:
            self.silhouette_avg = silhouette_score(self.feature_matrix, self.cluster_labels)
            
    def get_user_cluster(self, user_prefs: dict):
        """
        Predicts the cluster for a new user.
        """
        # Transform tags
        tags = user_prefs.get('tags', [])
        tag_matrix = self.mlb.transform([tags])
        
        # Transform categorical
        cat_data = pd.DataFrame([{
            'pref_budget': user_prefs.get('budget', 'medium'),
            'pref_climate': user_prefs.get('climate', 'moderate'),
            'pref_travel_type': user_prefs.get('travel_type', 'leisure')
        }])
        
        if cat_data['pref_climate'][0] is None:
            cat_data['pref_climate'] = 'moderate'
            
        cat_matrix = self.ohe.transform(cat_data).toarray()
        
        user_vec = np.hstack((tag_matrix, cat_matrix))
        cluster_id = self.kmeans.predict(user_vec)[0]
        
        return cluster_id
        
    def get_similar_users_stats(self, cluster_id: int):
        """
        Returns stats about users in the same cluster.
        """
        cluster_users = self.users[self.users['cluster'] == cluster_id]
        
        # Most common tags in this cluster
        all_tags = [tag for tags_list in cluster_users['pref_tags'] for tag in tags_list]
        top_tags = pd.Series(all_tags).value_counts().head(3).index.tolist()
        
        return {
            "cluster_id": int(cluster_id),
            "user_count": len(cluster_users),
            "top_interests": top_tags
        }
