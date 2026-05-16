import os
from dotenv import load_dotenv

load_dotenv()

MT5_LOGIN = int(os.getenv("MT5_LOGIN"))
MT5_PASSWORD = os.getenv("MT5_PASSWORD")
MT5_SERVER = os.getenv("MT5_SERVER")

SYMBOL = os.getenv("SYMBOL", "GOLD.i#")
LOT_SIZE = float(os.getenv("LOT_SIZE", 0.01))
SL_POINTS = float(os.getenv("SL_POINTS", 2.0))
TP_POINTS = float(os.getenv("TP_POINTS", 2.5))

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", 80))
