# Setup Instructions

## Prerequisites

- Python 3.8+ (for backend)
- Node.js 18+ and npm (for frontend)
- (Optional) OpenAI API key for enhanced AI features

## Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. (Optional) Set up OpenAI API key:
```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

5. Run the backend server:

Option 1 - Using the run script:
```bash
./run.sh
```

Option 2 - Using uvicorn directly:
```bash
cd src
export PYTHONPATH="${PYTHONPATH}:$(pwd)/.."
python -m uvicorn server:app --reload --host 0.0.0.0 --port 8001
```

Option 3 - From backend directory:
```bash
cd src
python server.py
```

The API will be available at `http://localhost:8001`

## Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Create a `.env.local` file (optional, defaults to localhost:8001):
```bash
echo "NEXT_PUBLIC_API_URL=http://localhost:8001" > .env.local
```

4. Run the development server:
```bash
npm run dev
```

The frontend will be available at `http://localhost:3001`

## Usage

1. Start the backend server first (port 8001)
2. Start the frontend server (port 3001)
3. Open your browser to `http://localhost:3001`
4. Select a project from the dropdown to view its health report

## API Endpoints

- `GET /api/projects` - List all projects
- `GET /api/projects/{project_id}` - Get project details
- `GET /api/projects/{project_id}/health` - Get comprehensive health report
- `GET /api/projects/{project_id}/health/score` - Get health score only
- `POST /api/analyze-sentiment` - Analyze sentiment of text

## Features

- **Health Score Calculation**: 5-dimension scoring system
- **Risk Detection**: Automated risk identification
- **AI Recommendations**: AI-powered actionable recommendations
- **Sentiment Analysis**: Communication sentiment tracking
- **Visual Dashboard**: Interactive web interface with charts

## Notes

- The system currently uses mock data. The data adapter is designed to support real API integrations in the future.
- If OpenAI API key is not provided, the system will use fallback keyword-based sentiment analysis and rule-based recommendations.

