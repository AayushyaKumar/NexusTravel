import React from 'react';
import { MapPin, Users, Navigation, Info, ShieldAlert, IndianRupee, ThermometerSun, Star, Tag } from 'lucide-react';
import type { MLResponse } from '../types';

interface ResultsProps {
  data: MLResponse;
}

const Results: React.FC<ResultsProps> = ({ data }) => {
  return (
    <div className="w-full max-w-6xl mx-auto space-y-8 animate-fade-in">
      
      {/* Overview & Insights */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-2xl p-6 shadow-lg border border-orange-100">
          <div className="flex items-center space-x-3 mb-4 text-teal-600">
            <Users size={24} />
            <h3 className="text-xl font-semibold text-slate-800">Traveler Persona Insight</h3>
          </div>
          <p className="text-slate-600 text-lg leading-relaxed">
            {data.similar_users_insight}
          </p>
          <div className="mt-4 pt-4 border-t border-slate-100 flex space-x-4 text-sm text-slate-500">
            <span className="flex items-center"><Info size={14} className="mr-1"/> ML Clustering: K-Means</span>
            <span>Silhouette: {data.clustering_evaluation.silhouette_score ?? 'N/A'}</span>
          </div>
        </div>

        <div className="bg-white rounded-2xl p-6 shadow-lg border border-orange-100">
          <div className="flex items-center space-x-3 mb-4 text-orange-500">
            <Navigation size={24} />
            <h3 className="text-xl font-semibold text-slate-800">Optimized Travel Route</h3>
          </div>
          <div className="flex flex-wrap items-center gap-2">
            {data.optimized_travel_route.map((stop, index) => (
              <React.Fragment key={stop.id}>
                <div className="bg-orange-50 border border-orange-200 px-3 py-1.5 rounded-lg text-orange-800 font-medium">
                  {stop.name}
                </div>
                {index < data.optimized_travel_route.length - 1 && (
                  <span className="text-slate-400 font-bold">→</span>
                )}
              </React.Fragment>
            ))}
          </div>
          <div className="mt-4 pt-4 border-t border-slate-100 flex space-x-4 text-sm text-slate-500">
            <span className="flex items-center"><Info size={14} className="mr-1"/> Heuristic: Nearest Neighbor (Haversine)</span>
          </div>
        </div>
      </div>

      {/* Top Recommendations */}
      <div>
        <h2 className="text-2xl font-bold text-slate-800 mb-6 flex items-center">
          <MapPin className="mr-2 text-rose-500" />
          Top Recommended Destinations
        </h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {data.recommendations.map((dest, i) => (
            <div key={dest.id} className="relative group rounded-2xl overflow-hidden bg-white shadow-xl border border-orange-100 hover:border-orange-400 hover:shadow-2xl transition-all duration-300 transform hover:-translate-y-1">
              <div className="h-48 bg-gradient-to-br from-orange-100 to-rose-100 p-6 flex flex-col justify-end relative overflow-hidden">
                <div className="absolute top-0 right-0 p-4">
                  <div className="bg-white/90 text-rose-600 text-xs font-bold px-3 py-1 rounded-full shadow-sm backdrop-blur-sm">
                    {(dest.similarity_score * 100).toFixed(1)}% Match
                  </div>
                </div>
                
                {/* Simulated map graphic in background */}
                <div className="absolute inset-0 opacity-20 pointer-events-none" 
                     style={{ backgroundImage: 'radial-gradient(circle at 2px 2px, #f43f5e 1px, transparent 0)', backgroundSize: '20px 20px' }}>
                </div>

                <h3 className="text-2xl font-bold text-slate-800 relative z-10 drop-shadow-sm">{dest.name}</h3>
                <div className="text-slate-600 text-sm mt-1 relative z-10 font-medium">
                  Lat: {dest.lat.toFixed(2)} / Lon: {dest.lon.toFixed(2)}
                </div>
              </div>
              <div className="p-6">
                {/* Metrics Row */}
                <div className="flex flex-wrap items-center gap-3 mb-4 border-b border-orange-50 pb-4">
                  <div className="flex items-center text-emerald-600 text-sm font-semibold bg-emerald-50 px-2 py-1 rounded-md">
                    <IndianRupee size={14} className="mr-0.5" />
                    <span>{dest.est_cost.toLocaleString()}</span>
                  </div>
                  <div className="flex items-center text-amber-600 text-sm font-semibold bg-amber-50 px-2 py-1 rounded-md">
                    <ThermometerSun size={14} className="mr-1" />
                    <span className="capitalize">{dest.climate}</span>
                  </div>
                  <div className="flex items-center text-yellow-600 text-sm font-semibold bg-yellow-50 px-2 py-1 rounded-md">
                    <Star size={14} className="mr-1" />
                    <span>{dest.ratings}</span>
                  </div>
                </div>

                <p className="text-slate-600 text-sm leading-relaxed mb-4">
                  {dest.reason}
                </p>

                {/* Tags */}
                <div className="flex flex-wrap gap-2 mt-auto">
                  {dest.tags.map(tag => (
                    <span key={tag} className="flex items-center text-xs font-medium text-slate-500 bg-slate-100 px-2 py-1 rounded-full">
                      <Tag size={10} className="mr-1" />
                      {tag}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Debug Info */}
      <div className="mt-12 bg-slate-50 rounded-xl p-4 border border-slate-200 shadow-inner">
        <h4 className="text-slate-500 text-xs font-semibold uppercase tracking-wider mb-2 flex items-center">
          <ShieldAlert size={14} className="mr-1" /> Parsed Query Parameters
        </h4>
        <pre className="text-teal-700 text-xs overflow-x-auto">
          {JSON.stringify(data.parsed_preferences, null, 2)}
        </pre>
      </div>
    </div>
  );
};

export default Results;
