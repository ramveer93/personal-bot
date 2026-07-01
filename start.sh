#!/bin/bash

# Start the uvicorn server
echo "Starting Uvicorn server..."
cd backend && ./venv/bin/python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000
