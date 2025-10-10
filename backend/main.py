
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from database import Base, engine, SessionLocal
import models, crud, schemas, deps
import os

app = FastAPI(title="DR Exercise Management API (Demo)")

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Create DB tables
Base.metadata.create_all(bind=engine)

@app.get('/api/health')
def health():
    return {'status': 'ok'}

# Devices / assets endpoints
@app.get('/api/devices', response_model=list[schemas.Device])
def list_devices():
    db = SessionLocal()
    return crud.get_devices(db)

@app.post('/api/devices', response_model=schemas.Device)
def create_device(device: schemas.DeviceCreate):
    db = SessionLocal()
    return crud.create_device(db, device)

@app.post('/api/devices/refresh')
def refresh_sample_data():
    db = SessionLocal()
    crud.delete_all_devices(db)
    crud.create_sample_devices(db)
    return {'status': 'ok'}

# Reports - aggregated recovery
@app.get('/api/reports/summary')
def recovery_summary():
    db = SessionLocal()
    return crud.recovery_summary(db)

# Upload documents (stores files in backend/uploads)
UPLOAD_DIR = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post('/api/upload')
def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, 'wb') as f:
        f.write(file.file.read())
    return {'filename': file.filename}

@app.get('/api/upload/{filename}')
def get_uploaded_file(filename: str):
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail='Not found')
    return FileResponse(file_path)
