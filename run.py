import uvicorn
from app.config import HOST, PORT

if __name__ == "__main__":
    print("Starting CRT Trading Bridge...")
    print(f"Listening on http://{HOST}:{PORT}")
    print(" Webhook endpoint: POST /webhook")

    uvicorn.run(
        "app.main:app",
        host=HOST,
        port=PORT,
        reload=False
    )
