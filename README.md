
# DR Exercise Management - Python Full Stack Demo

This demo contains a **FastAPI** backend and a **Streamlit** dashboard to visualize DR components, recovery percentages, and upload documents.

## Structure
- `backend/` - FastAPI backend with SQLite (dr_demo.db)
- `dashboard/` - Streamlit dashboard that calls backend APIs
- `scripts/` - Simple automation script that refreshes sample data periodically

## Run locally (recommended)
1. Create a virtual environment and activate it (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate   # mac/linux
   venv\Scripts\activate    # windows
   ```

2. Install backend requirements and run backend:
   ```bash
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload --port 8000
   ```

3. In a new terminal, run Streamlit dashboard:
   ```bash
   cd dashboard
   pip install -r requirements.txt
   streamlit run app.py
   ```

4. (Optional) Run the data collector script to auto-refresh sample data:
   ```bash
   python scripts/dr_data_collector.py
   ```

## Notes
- This is a demo scaffold. Add proper authentication, validation, and persistent storage for production use.
- Uploaded files are stored in `backend/uploads/`.
