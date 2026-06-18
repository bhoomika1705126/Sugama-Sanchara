#!/usr/bin/env bash

# ============================================================================
# Sugama Sanchara Frontend - Quick Start Setup
# ============================================================================

echo "🚀 Sugama Sanchara - Frontend Setup Script"
echo "==========================================="
echo ""

# Detect OS
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" || "$OSTYPE" == "cygwin" ]]; then
    echo "🪟 Detected: Windows"
    IS_WINDOWS=true
else
    echo "🐧 Detected: Unix-like OS (macOS/Linux)"
    IS_WINDOWS=false
fi

# ============================================================================
# Step 1: Create Virtual Environment
# ============================================================================

echo ""
echo "📦 Step 1: Creating Python Virtual Environment..."

if [ "$IS_WINDOWS" = true ]; then
    python -m venv venv
    venv\Scripts\activate
else
    python3 -m venv venv
    source venv/bin/activate
fi

echo "✅ Virtual environment created and activated"

# ============================================================================
# Step 2: Install Dependencies
# ============================================================================

echo ""
echo "📥 Step 2: Installing dependencies..."
echo "   This may take 2-3 minutes..."
echo ""

pip install --upgrade pip
pip install -r requirements.txt

echo ""
echo "✅ All dependencies installed successfully"

# ============================================================================
# Step 3: Configuration
# ============================================================================

echo ""
echo "⚙️  Step 3: Configuration"
echo ""

# Check if .env exists
if [ ! -f ".env" ]; then
    echo "Creating .env file from template..."
    cp .env.example .env
    echo "✅ .env file created. Edit if needed."
else
    echo "✅ .env file already exists"
fi

# ============================================================================
# Step 4: Ready to Run
# ============================================================================

echo ""
echo "🎉 Setup Complete!"
echo ""
echo "To start the dashboard, run:"
echo "    streamlit run app.py"
echo ""
echo "The application will open at:"
echo "    http://localhost:8501"
echo ""
echo "Make sure the backend is running at:"
echo "    http://localhost:8000"
echo ""
echo "API Endpoints to verify:"
echo "    GET  http://localhost:8000/"
echo "    POST http://localhost:8000/api/v1/operations/trigger"
echo "    GET  http://localhost:8000/api/v1/flipkart/logistics-update"
echo ""
echo "Happy coding! 🚦"
