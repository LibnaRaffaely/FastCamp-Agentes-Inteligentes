
1. python -m venv .venv

2. .venv\Scripts\Activate.ps1

3. pip install -r requirements.txt

4. Execução:
    - terminal: adk run app
    - web: adk web
    - app: uvicorn app.server:app --host 0.0.0.0 --port 8000

