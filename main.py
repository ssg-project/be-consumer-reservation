from app.consumer import start_consumer
import asyncio

if __name__ == '__main__':
    uvicorn.run(app, host="0.0.0.0", port=9093)