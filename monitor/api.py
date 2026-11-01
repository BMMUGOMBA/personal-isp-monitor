from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import FastAPI, Query
from fastapi.responses import FileResponse
from .config import Settings
from .storage import initialize, latest
from .probes import calculate_stats

@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize(Settings().database_path)
    yield

app = FastAPI(title='Personal ISP Monitor API', lifespan=lifespan)

@app.get('/')
def dashboard():
    return FileResponse(Path(__file__).resolve().parent.parent / 'web' / 'index.html')

@app.get('/api/health')
def health():
    return {'status': 'ok'}

@app.get('/api/measurements')
def measurements(limit: int = Query(100, ge=1, le=1000)):
    return latest(Settings().database_path, limit)

@app.get('/api/summary')
def summary(limit: int = Query(100, ge=1, le=1000)):
    return calculate_stats(latest(Settings().database_path, limit))
