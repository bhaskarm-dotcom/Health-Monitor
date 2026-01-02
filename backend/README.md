# Backend - AI Project Health Monitor

FastAPI backend for the AI-Powered Project Health Monitor system.

## Structure

- `src/models.py` - Pydantic data models
- `src/mock_data.py` - Mock data generator
- `src/health_calculator.py` - Health score calculation engine
- `src/ai_service.py` - AI integration for sentiment and recommendations
- `src/data_adapter.py` - Data abstraction layer
- `src/server.py` - FastAPI application
- `src/config.py` - Configuration management

## Running the Server

```bash
# From backend directory
cd src
python server.py
```

Or with uvicorn:
```bash
uvicorn src.server:app --reload
```

## API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8001/docs`
- ReDoc: `http://localhost:8001/redoc`

