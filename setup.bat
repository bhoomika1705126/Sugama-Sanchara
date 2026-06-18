@echo off
REM ============================================================================
REM Sugama Sanchara Frontend - Quick Start Setup (Windows)
REM ============================================================================

echo.
echo ======================================================================
echo   SUGAMA SANCHARA - FRONTEND SETUP (Windows)
echo ======================================================================
echo.

REM ============================================================================
REM Step 1: Create Virtual Environment
REM ============================================================================

echo [1/4] Creating Python Virtual Environment...
echo.

if not exist venv (
    python -m venv venv
    echo Virtual environment created successfully
) else (
    echo Virtual environment already exists
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo ✓ Virtual environment activated

REM ============================================================================
REM Step 2: Install Dependencies
REM ============================================================================

echo.
echo [2/4] Installing dependencies...
echo This may take 2-3 minutes...
echo.

python -m pip install --upgrade pip
pip install -r requirements.txt

if errorlevel 1 (
    echo.
    echo ✗ Failed to install dependencies
    echo Please check your internet connection and try again
    pause
    exit /b 1
)

echo.
echo ✓ All dependencies installed successfully

REM ============================================================================
REM Step 3: Configuration
REM ============================================================================

echo.
echo [3/4] Setting up configuration...
echo.

if not exist .env (
    copy .env.example .env
    echo ✓ .env file created from template
    echo.
    echo Edit .env if you need to change the API URL
) else (
    echo ✓ .env file already exists
)

REM ============================================================================
REM Step 4: Verification
REM ============================================================================

echo.
echo [4/4] Verifying setup...
echo.

python --version
echo ✓ Python installed

pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo ✗ Streamlit not found
    pause
    exit /b 1
) else (
    echo ✓ Streamlit installed
)

echo.
echo ======================================================================
echo   SETUP COMPLETE!
echo ======================================================================
echo.
echo To start the dashboard, run:
echo.
echo     streamlit run app.py
echo.
echo The application will open at:
echo     http://localhost:8501
echo.
echo Important: Make sure the backend is running at:
echo     http://localhost:8000
echo.
echo Backend Setup:
echo   1. Navigate to the backend folder
echo   2. Create virtual environment: python -m venv venv
echo   3. Activate: venv\Scripts\activate
echo   4. Install: pip install -r requirements.txt
echo   5. Run: python -m uvicorn src.api:app --reload --host 0.0.0.0
echo.
echo Verify API is running with:
echo   curl http://localhost:8000/
echo.
echo Frontend commands:
echo   - streamlit run app.py                 [Start frontend]
echo   - streamlit config show                 [Show config]
echo   - streamlit cache clear                 [Clear cache]
echo.
echo For more help, see:
echo   - README.md (setup & features)
echo   - FEATURES.md (judge presentation tips)
echo.
echo ======================================================================
echo.

pause
