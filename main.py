from fastapi import FastAPI
from app.consumer import start_consumer
from ticket_router import ticket_router
import asyncio
import uvicorn

app = FastAPI()

# health check route
@app.get("/health")
async def health_check():
    return {"status": "ok"}

# router 설정
app.include_router(ticket_router, prefix="/api/v1", tags=["ticket"])

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9093)