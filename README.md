# Jina Knowledge Base Search

This is a search engine for Stack Overflow *questions* (i.e. not answers). It will return matching questions with associated answers from a given dataset.

## Run

### Backend

1. `cd backend`
2. `python app.py`

### Frontend

1. `cd frontend`
2. `python frontend.py`

## Configure

- **Backend:** `backend/config.py`
- **Frontend:** `frontend/config.py` and `frontend/.streamlit/config.toml`

## Deploy

`docker-compose up`
