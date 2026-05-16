import MetaTrader5 as mt5
from app.config import (
    MT5_LOGIN,
    MT5_PASSWORD,
    MT5_SERVER,
    SYMBOL,
    LOT_SIZE,
    SL_POINTS,
    TP_POINTS
)


def connect_mt5():
    if not mt5.initialize(
        login=MT5_LOGIN,
        server=MT5_SERVER,
        password=MT5_PASSWORD
    ):
        print(f"[ERROR] MT5 connection failed: {mt5.last_error()}")
        return False

    print(f"[OK] MT5 connected — Account: {MT5_LOGIN}")
    return True


def process_trade(data: dict):

    action = data.get("action", "").lower()
    comment = data.get("comment", "")

    if "Reset" in comment or "Internal" in comment:
        print(f"[SKIP] Housekeeping signal ignored: {comment}")
        return

    tick = mt5.symbol_info_tick(SYMBOL)

    if tick is None:
        print(f"[ERROR] Cannot fetch price for {SYMBOL}")
        return

    if action == "buy" and "Long Entry new" in comment:
        order_type = mt5.ORDER_TYPE_SELL
        price = tick.bid
        sl = round(price + 3.5, 2)
        tp = round(price - 3.5, 2)

    elif action == "sell" and "Short Entry new" in comment:
        order_type = mt5.ORDER_TYPE_BUY
        price = tick.ask
        sl = round(price - 3.5, 2)
        tp = round(price + 3.5, 2)

    elif action == "buy" and "Long Entry" in comment:
        order_type = mt5.ORDER_TYPE_BUY
        price = tick.ask
        sl = round(price - SL_POINTS, 2)
        tp = round(price + TP_POINTS, 2)

    elif action == "sell" and "Short Entry" in comment:
        order_type = mt5.ORDER_TYPE_SELL
        price = tick.bid
        sl = round(price + SL_POINTS, 2)
        tp = round(price - TP_POINTS, 2)

    else:
        print(f"[SKIP] Unrecognized signal: action={action}, comment={comment}")
        return

    request = {
        "action": mt5.TRADE_ACTION_DEAL,
        "symbol": SYMBOL,
        "volume": LOT_SIZE,
        "type": order_type,
        "price": price,
        "sl": sl,
        "tp": tp,
        "magic": 1540,
        "comment": f"TV: {comment}",
        "type_time": mt5.ORDER_TIME_GTC,
        "type_filling": mt5.ORDER_FILLING_IOC,
    }

    result = mt5.order_send(request)

    if result.retcode != mt5.TRADE_RETCODE_DONE:
        print(f"[FAILED] Trade failed: {result.comment}")
    else:
        print(
            f"[SUCCESS] {comment} → type={order_type} "
            f"price={price} sl={sl} tp={tp}"
        )
