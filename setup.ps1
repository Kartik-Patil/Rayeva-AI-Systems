# ============================================================================
# Rayeva AI Systems - Setup Script
# ============================================================================
# This script helps you set up the Rayeva AI Systems project
# ============================================================================

Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Rayeva AI Systems - Setup Script" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check Python version
Write-Host "[1/7] Checking Python version..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($pythonVersion -match "Python 3\.([9-9]|[1-9][0-9])") {
    Write-Host "  ✓ Python version OK: $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ Python 3.9+ required. Current: $pythonVersion" -ForegroundColor Red
    exit 1
}

# Create virtual environment
Write-Host "`n[2/7] Creating virtual environment..." -ForegroundColor Yellow
if (Test-Path "venv") {
    Write-Host "  ! Virtual environment already exists, skipping..." -ForegroundColor Yellow
} else {
    python -m venv venv
    Write-Host "  ✓ Virtual environment created" -ForegroundColor Green
}

# Activate virtual environment
Write-Host "`n[3/7] Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"
Write-Host "  ✓ Virtual environment activated" -ForegroundColor Green

# Install dependencies
Write-Host "`n[4/7] Installing dependencies..." -ForegroundColor Yellow
pip install -r requirements.txt --quiet
Write-Host "  ✓ Dependencies installed" -ForegroundColor Green

# Setup environment file
Write-Host "`n[5/7] Setting up environment file..." -ForegroundColor Yellow
if (Test-Path ".env") {
    Write-Host "  ! .env file already exists, skipping..." -ForegroundColor Yellow
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "  ✓ .env file created from template" -ForegroundColor Green
    Write-Host "  ⚠ IMPORTANT: Edit .env and add your OPENAI_API_KEY!" -ForegroundColor Red
}

# Create logs directory
Write-Host "`n[6/7] Creating logs directory..." -ForegroundColor Yellow
if (!(Test-Path "logs")) {
    New-Item -ItemType Directory -Path "logs" | Out-Null
    Write-Host "  ✓ Logs directory created" -ForegroundColor Green
} else {
    Write-Host "  ! Logs directory already exists" -ForegroundColor Yellow
}

# Initialize database
Write-Host "`n[7/7] Initializing database..." -ForegroundColor Yellow
python -c "import asyncio; from src.core.database import init_database; asyncio.run(init_database())"
Write-Host "  ✓ Database initialized" -ForegroundColor Green

# Final instructions
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "  Setup Complete! 🎉" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Edit .env file and add your OPENAI_API_KEY" -ForegroundColor White
Write-Host "  2. Run the application: python main.py" -ForegroundColor White
Write-Host "  3. Visit http://localhost:8000/docs for API documentation`n" -ForegroundColor White

Write-Host "Useful commands:" -ForegroundColor Yellow
Write-Host "  • Start API:        python main.py" -ForegroundColor White
Write-Host "  • Run tests:        pytest tests/ -v" -ForegroundColor White
Write-Host "  • Check coverage:   pytest --cov=src tests/" -ForegroundColor White
Write-Host "  • View API docs:    http://localhost:8000/docs`n" -ForegroundColor White

Write-Host "For more information, see README.md`n" -ForegroundColor Cyan
