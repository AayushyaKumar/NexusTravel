import React, { useState } from 'react';
import { Sparkles, Search, Compass, Globe2, SlidersHorizontal, Wand2, Plus, X } from 'lucide-react';
import Results from './components/Results';
import type { MLResponse } from './types';

// Function to call our Python ML backend API
const fetchMLResponse = async (queryData: any, isStructured: boolean): Promise<MLResponse> => {
  try {
    const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:8000';
    const response = await fetch(`${apiUrl}/api/recommend`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        isStructured,
        data: queryData
      })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
  } catch (error) {
    console.error("Backend unreachable, falling back to mock:", error);
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve({
        parsed_preferences: isStructured ? {
          budget: queryData.budgetMax <= 1000 ? "low" : queryData.budgetMax <= 2500 ? "medium" : "high",
          climate: queryData.climate || "moderate",
          travel_type: queryData.travelType || "leisure",
          tags: queryData.interests.map((t: string) => t.toLowerCase())
        } : {
          budget: "medium",
          climate: "moderate",
          travel_type: "leisure",
          tags: ["history", "cultural"]
        },
        clustering_evaluation: {
          inertia: 229.98,
          silhouette_score: 0.129
        },
        recommendations: [
          {
            id: 5,
            name: "Kyoto, Japan",
            similarity_score: 0.948,
            reason: "This destination matches your budget and climate preferences, along with interests in culture and history.",
            cost: "medium",
            est_cost: 150000,
            climate: "moderate",
            ratings: 4.9,
            tags: ["cultural", "history", "nature"],
            lat: 35.0116,
            lon: 135.7681
          },
          {
            id: 9,
            name: "Rome, Italy",
            similarity_score: 0.928,
            reason: "This destination has a medium cost and moderate climate, and matches your interest in cultural, history.",
            cost: "medium",
            est_cost: 160000,
            climate: "moderate",
            ratings: 4.7,
            tags: ["history", "food", "cultural"],
            lat: 41.9028,
            lon: 12.4964
          },
          {
            id: 6,
            name: "Machu Picchu, Peru",
            similarity_score: 0.801,
            reason: "This destination has a medium cost and moderate climate, and matches your interest in history.",
            cost: "medium",
            est_cost: 120000,
            climate: "moderate",
            ratings: 4.8,
            tags: ["history", "adventure", "nature"],
            lat: -13.1631,
            lon: -72.545
          },
          {
            id: 1,
            name: "Bali, Indonesia",
            similarity_score: 0.733,
            reason: "This destination has a medium cost and warm climate, and matches your general profile.",
            cost: "medium",
            est_cost: 100000,
            climate: "warm",
            ratings: 4.8,
            tags: ["beach", "nature", "nightlife", "leisure"],
            lat: -8.4095,
            lon: 115.1889
          },
          {
            id: 2,
            name: "Paris, France",
            similarity_score: 0.567,
            reason: "This destination has a high cost and moderate climate, and matches your interest in cultural, history.",
            cost: "high",
            est_cost: 280000,
            climate: "moderate",
            ratings: 4.7,
            tags: ["cultural", "history", "food", "leisure"],
            lat: 48.8566,
            lon: 2.3522
          }
        ],
        similar_users_insight: "Users like you (Cluster 3) also enjoy nightlife, history, leisure.",
        optimized_travel_route: [
          { id: 5, name: "Kyoto, Japan" },
          { id: 1, name: "Bali, Indonesia" },
          { id: 9, name: "Rome, Italy" },
          { id: 2, name: "Paris, France" },
          { id: 6, name: "Machu Picchu, Peru" }
        ]
      });
    }, 500);
  });
  }
};

const AVAILABLE_INTERESTS = ['Nature', 'Beaches', 'Mountains', 'Nightlife', 'Food', 'History', 'Shopping'];

function App() {
  const [inputMode, setInputMode] = useState<'prompt' | 'structured'>('prompt');
  
  // Prompt State
  const [query, setQuery] = useState('');
  
  // Structured State
  const [budgetMin, setBudgetMin] = useState<number>(20000);
  const [budgetMax, setBudgetMax] = useState<number>(100000);
  const [duration, setDuration] = useState<number>(7);
  const [travelType, setTravelType] = useState<string>('Leisure');
  const [climate, setClimate] = useState<string>('moderate');
  const [interests, setInterests] = useState<string[]>([]);
  
  // Global State
  const [isSearching, setIsSearching] = useState(false);
  const [result, setResult] = useState<MLResponse | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (inputMode === 'prompt' && !query.trim()) return;

    setIsSearching(true);
    setResult(null);

    try {
      const data = inputMode === 'prompt' ? query : {
        budgetMin, budgetMax, duration, travelType, climate, interests
      };
      const response = await fetchMLResponse(data, inputMode === 'structured');
      setResult(response);
      console.log(result);
    } catch (error) {
      console.error(error);
    } finally {
      setIsSearching(false);
    }
  };

  const toggleInterest = (interest: string) => {
    if (interests.includes(interest)) {
      setInterests(interests.filter(i => i !== interest));
    } else {
      setInterests([...interests, interest]);
    }
  };

  return (
    <div className="min-h-screen bg-[#faf9f6] text-slate-800 selection:bg-orange-500/30 font-sans relative overflow-x-hidden pb-12">
      {/* Dynamic Background */}
      <div className="fixed top-[-20%] left-[-10%] w-[50%] h-[50%] rounded-full bg-orange-400/20 blur-[120px] pointer-events-none" />
      <div className="fixed bottom-[-20%] right-[-10%] w-[50%] h-[50%] rounded-full bg-teal-400/20 blur-[120px] pointer-events-none" />
      
      {/* Navigation */}
      <nav className="relative z-10 border-b border-orange-200/50 bg-white/50 backdrop-blur-md">
        <div className="max-w-7xl mx-auto px-6 h-20 flex items-center justify-between">
          <div className="flex items-center space-x-3 cursor-pointer group">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-orange-400 to-rose-500 flex items-center justify-center shadow-lg group-hover:shadow-orange-500/25 transition-all">
              <Globe2 className="text-white" size={20} />
            </div>
            <span className="text-xl font-bold tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-orange-600 to-rose-600">
              NexusTravel
            </span>
          </div>
          
        </div>
      </nav>

      {/* Hero Section */}
      <main className="relative z-10 flex flex-col items-center justify-center pt-16 pb-12 px-4">
        <div className="text-center max-w-3xl mx-auto animate-fade-in w-full">
          <div className="inline-flex items-center px-4 py-2 rounded-full border border-orange-200 bg-orange-50 text-orange-600 text-sm font-medium mb-8 shadow-sm">
            <Sparkles size={16} className="mr-2" />
            AI-Powered Travel Recommendations
          </div>
          <h1 className="text-5xl md:text-6xl font-extrabold tracking-tight mb-6 leading-tight text-slate-900">
            Discover Your Next <br/>
            <span className="bg-clip-text text-transparent bg-gradient-to-r from-orange-500 via-rose-500 to-pink-500">
              Perfect Journey
            </span>
          </h1>
          
          {/* Mode Toggle */}
          <div className="flex justify-center mb-8">
            <div className="bg-white p-1 rounded-xl shadow-md border border-orange-100 inline-flex">
              <button 
                onClick={() => setInputMode('prompt')}
                className={`flex items-center px-6 py-2.5 rounded-lg text-sm font-medium transition-all ${inputMode === 'prompt' ? 'bg-orange-100 text-orange-700 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
              >
                <Wand2 size={16} className="mr-2" /> Magic Prompt
              </button>
              <button 
                onClick={() => setInputMode('structured')}
                className={`flex items-center px-6 py-2.5 rounded-lg text-sm font-medium transition-all ${inputMode === 'structured' ? 'bg-orange-100 text-orange-700 shadow-sm' : 'text-slate-500 hover:text-slate-700'}`}
              >
                <SlidersHorizontal size={16} className="mr-2" /> Exact Filters
              </button>
            </div>
          </div>

          <form onSubmit={handleSearch} className="relative group max-w-3xl mx-auto text-left">
            <div className="absolute inset-0 bg-gradient-to-r from-orange-400 to-teal-400 rounded-2xl blur opacity-20 group-hover:opacity-30 transition duration-500"></div>
            <div className="relative bg-white rounded-2xl p-6 border border-orange-100 shadow-xl focus-within:border-orange-300 transition-colors">
              
              {inputMode === 'prompt' ? (
                <div>
                  <div className="flex items-center">
                    <Compass size={24} className="text-orange-500 mr-3" />
                    <input 
                      type="text" 
                      value={query}
                      onChange={(e) => setQuery(e.target.value)}
                      placeholder="e.g., 'A cheap beach vacation with good nightlife'"
                      className="w-full bg-transparent border-none text-slate-800 text-lg placeholder-slate-400 focus:outline-none py-2"
                    />
                  </div>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-6 pb-2">
                  {/* Budget */}
                  <div className="space-y-2">
                    <label className="block text-sm font-semibold text-slate-700">Budget Range (INR ₹)</label>
                    <div className="flex items-center space-x-2">
                      <input type="number" value={budgetMin} onChange={e => setBudgetMin(Number(e.target.value))} className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-slate-700 focus:ring-2 focus:ring-orange-500 focus:outline-none" placeholder="Min" />
                      <span className="text-slate-400">-</span>
                      <input type="number" value={budgetMax} onChange={e => setBudgetMax(Number(e.target.value))} className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-slate-700 focus:ring-2 focus:ring-orange-500 focus:outline-none" placeholder="Max" />
                    </div>
                  </div>

                  {/* Duration */}
                  <div className="space-y-2">
                    <label className="block text-sm font-semibold text-slate-700">Trip Duration (Days)</label>
                    <input type="number" min="1" max="60" value={duration} onChange={e => setDuration(Number(e.target.value))} className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-slate-700 focus:ring-2 focus:ring-orange-500 focus:outline-none" />
                  </div>

                  {/* Travel Type */}
                  <div className="space-y-2">
                    <label className="block text-sm font-semibold text-slate-700">Travel Type</label>
                    <select value={travelType} onChange={e => setTravelType(e.target.value)} className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-slate-700 focus:ring-2 focus:ring-orange-500 focus:outline-none appearance-none">
                      <option value="Adventure">Adventure</option>
                      <option value="Leisure">Leisure</option>
                      <option value="Solo">Solo</option>
                      <option value="Family">Family</option>
                    </select>
                  </div>

                  {/* Climate */}
                  <div className="space-y-2">
                    <label className="block text-sm font-semibold text-slate-700">Preferred Climate</label>
                    <select value={climate} onChange={e => setClimate(e.target.value)} className="w-full bg-slate-50 border border-slate-200 rounded-lg px-3 py-2 text-slate-700 focus:ring-2 focus:ring-orange-500 focus:outline-none appearance-none">
                      <option value="warm">Warm / Tropical</option>
                      <option value="moderate">Moderate / Mild</option>
                      <option value="cold">Cold / Winter</option>
                    </select>
                  </div>

                  {/* Interests */}
                  <div className="col-span-1 md:col-span-2 space-y-2">
                    <label className="block text-sm font-semibold text-slate-700">Interests</label>
                    <div className="flex flex-wrap gap-2">
                      {AVAILABLE_INTERESTS.map(interest => (
                        <button
                          key={interest}
                          type="button"
                          onClick={() => toggleInterest(interest)}
                          className={`px-3 py-1.5 rounded-full border text-sm font-medium transition-all ${
                            interests.includes(interest) 
                            ? 'bg-orange-500 border-orange-500 text-white shadow-md' 
                            : 'bg-white border-slate-300 text-slate-600 hover:border-orange-300 hover:bg-orange-50'
                          }`}
                        >
                          {interests.includes(interest) ? <X size={14} className="inline mr-1"/> : <Plus size={14} className="inline mr-1"/>}
                          {interest}
                        </button>
                      ))}
                    </div>
                  </div>
                </div>
              )}

              <div className={`flex justify-end ${inputMode === 'structured' ? 'mt-6 pt-6 border-t border-slate-100' : ''}`}>
                <button 
                  type="submit"
                  disabled={isSearching || (inputMode === 'prompt' && !query.trim())}
                  className={`bg-gradient-to-r from-orange-500 to-rose-500 hover:from-orange-600 hover:to-rose-600 disabled:from-slate-300 disabled:to-slate-300 disabled:text-slate-500 text-white rounded-xl font-semibold transition-all flex items-center shadow-md shadow-orange-500/20 ${inputMode === 'structured' ? 'px-8 py-3' : 'px-6 py-2 absolute right-2 top-2'}`}
                >
                  {isSearching ? (
                    <span className="flex items-center">
                      <svg className="animate-spin -ml-1 mr-2 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                      </svg>
                      Analyzing...
                    </span>
                  ) : (
                    <span className="flex items-center">
                      <Search size={18} className="mr-2" />
                      Explore
                    </span>
                  )}
                </button>
              </div>
            </div>
          </form>
        </div>
      </main>

      {/* Results Section */}
      {result && (
        <section className="relative z-10 px-4 pb-24 pt-8 border-t border-orange-100 bg-white/40">
          <Results data={result} />
          
        </section>
      )}
    </div>
  );
}

export default App;
