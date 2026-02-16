#!/bin/bash

echo "🚀 AI Market Intelligence Hub - Quick Start"
echo "==========================================="

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "⚠️  .env file not found. Copying from .env.example..."
    cp .env.example .env
    echo "⚠️  Please edit .env with your API keys before running pipelines"
fi

# Create data directories
mkdir -p data/warehouse data/raw

echo ""
echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env with your API keys"
echo "2. Run ingestion: python -m ingestion.pipelines.news_pipeline"
echo "3. Run dbt: cd transformation && dbt run --profiles-dir ."
echo "4. Start API: cd api && uvicorn main:app --reload"
echo ""
echo "Or run the full pipeline with Airflow (see SETUP.md)"
