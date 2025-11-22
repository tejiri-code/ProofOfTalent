#!/bin/bash

# Start script for UK Global Talent Visa Analysis API

echo "Starting UK Global Talent Visa Analysis API..."

# Check if OpenAI API key is set
if [ -z "$OPENAI_API_KEY" ]; then
    echo "Warning: OPENAI_API_KEY is not set!"
    echo "Set it with: export OPENAI_API_KEY='your-api-key'"
    echo ""
fi

# Navigate to app directory
cd "$(dirname "$0")/app"

# Start server
echo "Server starting at http://localhost:8000"
echo "API docs available at http://localhost:8000/docs"
echo ""

python main.py
