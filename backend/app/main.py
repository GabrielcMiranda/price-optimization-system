from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers.auth_router import auth_router
import uvicorn
from app.routers.optimization_router import optimization_router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

app.include_router(auth_router)
app.include_router(optimization_router)
@app.get('/')
def home():
    return {'message': 'Backend está funcionando!', 'status': 'ok', 'app': 'price-optimization-system'}

@app.get('/health')
def health_check():
    return {'status': 'healthy'}
    
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 