FROM python:3.11-slim

WORKDIR /app

# Install Python requirements
COPY backend/requirements.txt backend/requirements.txt
RUN pip install --no-cache-dir -r backend/requirements.txt

# Copy backend, data and built frontend
COPY backend/ backend/
COPY data/ data/
COPY frontend/dist/ frontend/dist/

ENV PORT=8000
EXPOSE 8000

CMD uvicorn backend.main:app --host 0.0.0.0 --port ${PORT:-8000}
