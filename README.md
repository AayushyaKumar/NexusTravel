# AI Travel Planner

AI Travel Planner is a full-stack web application designed to help users discover their ideal travel destinations. Powered by a custom Machine Learning core, the app provides tailored recommendations based on user preferences. It supports two intuitive ways to search:

- **Natural Language Prompting:** Simply type the trip details. (e.g., "I want a cheap beach vacation with good nightlife").
- **Structured Filtering:** Use specific filters such as budget (in INR), duration, climate, travel type, and interests to pinpoint exactly what users looking for.

The application computes an estimated budget, optimal duration, and generates a smart itinerary route, comparing both domestic (India) and international locations.

## Tech Stack

- **Backend:** Python, FastAPI, Custom ML Engine
- **Frontend:** React, TypeScript, Vite, TailwindCSS

## How to Run the Application

The project is split into a FastAPI backend and a React frontend. You will need to run both concurrently.

### 1. Running the Backend (FastAPI)

The backend provides the API for the machine learning engine. From the root directory:

```bash
# Optional: Create and activate a virtual environment
# python -m venv venv
# .\venv\Scripts\activate

# Install required Python packages
pip install fastapi uvicorn pydantic

# Run the FastAPI server
uvicorn main:app --reload
```

_The backend server will typically start on http://127.0.0.1:8000._

### 2. Running the Frontend (React / Vite)

The frontend provides the user interface. Open a new terminal and navigate to the `frontend` directory:

```bash
# Navigate to the frontend directory
cd frontend

# Install Node.js dependencies
npm install

# Start the Vite development server
npm run dev
```

_The frontend server will typically start on http://localhost:5173._
