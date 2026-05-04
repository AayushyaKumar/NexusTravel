import math

class RouteOptimizer:
    """
    Given a list of selected destinations, suggests an optimal travel order.
    Uses a simple nearest-neighbor (greedy) heuristic.
    """
    @staticmethod
    def haversine_distance(lat1, lon1, lat2, lon2):
        """Calculates distance between two lat/lon points in km."""
        R = 6371.0 # Earth radius in km
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        
        return R * c

    def optimize_route(self, destinations: list):
        """
        Orders the destinations using a greedy nearest-neighbor approach.
        Starts with the first destination in the list.
        """
        if not destinations:
            return []
            
        unvisited = destinations.copy()
        current = unvisited.pop(0)
        route = [current]
        
        while unvisited:
            # Find the nearest unvisited destination
            nearest_dist = float('inf')
            nearest_dest = None
            
            for dest in unvisited:
                dist = self.haversine_distance(
                    current['lat'], current['lon'],
                    dest['lat'], dest['lon']
                )
                if dist < nearest_dist:
                    nearest_dist = dist
                    nearest_dest = dest
                    
            route.append(nearest_dest)
            unvisited.remove(nearest_dest)
            current = nearest_dest
            
        # Return simplified route info
        return [{"id": d["id"], "name": d["name"]} for d in route]
