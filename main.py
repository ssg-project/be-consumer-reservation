from app.consumer import start_consumer
from fastapi import FastAPI
import asyncio

app = FastAPI() 

@app.get("/health")
async def health_check():
    return {"status": "ok"}

if __name__ == '__main__':
    asyncio.run(start_consumer())