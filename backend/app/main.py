from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get('/')
def home():
    return {'message': 'Backend está funcionando!', 'status': 'ok', 'app': 'price-optimization-system'}

@app.get('/health')
def health_check():
    return {'status': 'healthy'}
    
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True) 