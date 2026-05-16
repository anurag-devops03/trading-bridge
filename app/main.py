from fastapi import FastAPI, Request, BackgroundTasks
from app.trader import connect_mt5, process_trade

app = FastAPI(
    title="CRT Trading Bridge",
    description="TradingView → FastAPI → MetaTrader5 live trade executor",
    version="1.0.0"
)


@app.on_event("startup")
async def startup_event():
    connect_mt5()


@app.get("/")
async def health_check():
    return {
        "status": "online",
        "message": "CRT Trading Bridge is running"
    }


@app.post("/webhook")
async def webhook(request: Request, background_tasks: BackgroundTasks):

    payload = await request.json()

    print(f"[WEBHOOK] Received: {payload}")

    background_tasks.add_task(process_trade, payload)

    return {"status": "received"}
