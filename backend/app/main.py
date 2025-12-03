from fastapi import FastAPI
from app.routers.auth_router import auth_router
import uvicorn

app = FastAPI()

app.include_router(auth_router)

@app.get('/')
def home():
    return {'message': 'Backend está funcionando!', 'status': 'ok', 'app': 'price-optimization-system'}

@app.get('/health')
def health_check():
    return {'status': 'healthy'}
    
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 