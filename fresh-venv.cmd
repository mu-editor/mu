IF EXIST .venv (rmdir /s/q .venv) && py -3 -mvenv .venv && .venv\scripts\python -mpip install --upgrade pip && .venv\scripts\pip install -e .[dev] && .venv\scripts\activate
PAUSE
