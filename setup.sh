#!/bin/bash

# ============================================================================
# Rayeva AI Systems - Setup Script (Linux/Mac)
# ============================================================================

echo ""
echo "========================================"
echo "  Rayeva AI Systems - Setup Script"
echo "========================================"
echo ""

# Check Python version
echo "[1/7] Checking Python version..."
python_version=$(python3 --version 2>&1 | grep -oP '\d+\.\d+')
if [[ $(echo "$python_version >= 3.9" | bc) -eq 1 ]]; then
    echo "  ✓ Python version OK: $(python3 --version)"
else
    echo "  ✗ Python 3.9+ required. Current: $(python3 --version)"
    exit 1
fi

# Create virtual environment
echo ""
echo "[2/7] Creating virtual environment..."
if [ -d "venv" ]; then
    echo "  ! Virtual environment already exists, skipping..."
else
    python3 -m venv venv
    echo "  ✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "[3/7] Activating virtual environment..."
source venv/bin/activate
echo "  ✓ Virtual environment activated"

# Install dependencies
echo ""
echo "[4/7] Installing dependencies..."
pip install -r requirements.txt --quiet
echo "  ✓ Dependencies installed"

# Setup environment file
echo ""
echo "[5/7] Setting up environment file..."
if [ -f ".env" ]; then
    echo "  ! .env file already exists, skipping..."
else
    cp .env.example .env
    echo "  ✓ .env file created from template"
    echo "  ⚠ IMPORTANT: Edit .env and add your OPENAI_API_KEY!"
fi

# Create logs directory
echo ""
echo "[6/7] Creating logs directory..."
if [ ! -d "logs" ]; then
    mkdir logs
    echo "  ✓ Logs directory created"
else
    echo "  ! Logs directory already exists"
fi

# Initialize database
echo ""
echo "[7/7] Initializing database..."
python3 -c "import asyncio; from src.core.database import init_database; asyncio.run(init_database())"
echo "  ✓ Database initialized"

# Final instructions
echo ""
echo "========================================"
echo "  Setup Complete! 🎉"
echo "========================================"
echo ""

echo "Next steps:"
echo "  1. Edit .env file and add your OPENAI_API_KEY"
echo "  2. Run the application: python3 main.py"
echo "  3. Visit http://localhost:8000/docs for API documentation"
echo ""

echo "Useful commands:"
echo "  • Start API:        python3 main.py"
echo "  • Run tests:        pytest tests/ -v"
echo "  • Check coverage:   pytest --cov=src tests/"
echo "  • View API docs:    http://localhost:8000/docs"
echo ""

echo "For more information, see README.md"
echo ""
