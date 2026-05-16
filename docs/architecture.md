# System Architecture — CRT Trading Bridge

## Overview

This document explains the complete architecture of the automated
trading infrastructure. The system connects TradingView signals
to MetaTrader 5 for live trade execution on GOLD (XAUUSD).

---

## Full System Flow
┌─────────────────────────────────────────────────────────┐
│                    TRADINGVIEW                          │
│         CRT TBS v17.5 — Pine Script Strategy            │
│                                                         │
│   Monitors GOLD chart → detects CRT candle pattern      │
│   Applies cooldown (10 bars) → filters bad signals      │
│   Fires webhook alert with action + comment             │
└─────────────────────┬───────────────────────────────────┘
│
│  HTTP POST /webhook
│  {
│    "action": "buy",
│    "comment": "Long Entry new"
│  }
▼
┌─────────────────────────────────────────────────────────┐
│              AWS EC2 — Windows Server                   │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │           FastAPI Bridge (main.py)                │  │
│  │                                                   │  │
│  │   POST /webhook received                          │  │
│  │        │                                          │  │
│  │        ▼                                          │  │
│  │   BackgroundTask → process_trade()                │  │
│  │        │                                          │  │
│  │        ▼                                          │  │
│  │   Filter: Reset/Internal? → SKIP                  │  │
│  │        │                                          │  │
│  │        ▼                                          │  │
│  │   Route Signal:                                   │  │
│  │   ├── "Long Entry new"  → SELL (fade logic)       │  │
│  │   ├── "Short Entry new" → BUY  (fade logic)       │  │
│  │   ├── "Long Entry"      → BUY  (standard)         │  │
│  │   └── "Short Entry"     → SELL (standard)         │  │
│  │        │                                          │  │
│  │        ▼                                          │  │
│  │   Build MT5 order request                         │  │
│  │   (symbol, volume, type, price, sl, tp)           │  │
│  └───────────────────┬───────────────────────────────┘  │
│                      │                                  │
│  ┌───────────────────▼───────────────────────────────┐  │
│  │           MetaTrader 5 Terminal                   │  │
│  │                                                   │  │
│  │   Broker:  XM Global                              │  │
│  │   Symbol:  GOLD.i#                                │  │
│  │   Lot:     0.01                                   │  │
│  │   Magic:   1540                                   │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
│
▼
✅ LIVE TRADE EXECUTED
---

## Signal Routing Logic

| TradingView Signal | Comment Tag | MT5 Action | SL/TP |
|---|---|---|---|
| BUY | Long Entry new | SELL (fade) | 3.5 / 3.5 |
| SELL | Short Entry new | BUY (fade) | 3.5 / 3.5 |
| BUY | Long Entry | BUY (standard) | 2.0 / 2.5 |
| SELL | Short Entry | SELL (standard) | 2.0 / 2.5 |
| ANY | Reset / Internal | SKIP | — |

---

## CRT Strategy Logic

| Concept | Detail |
|---|---|
| Indicator | CRT — Candle Range Theory |
| Timeframe | Any (designed for lower timeframes) |
| Asset | GOLD (XAUUSD) |
| CRT Candle | Body ≥ 50% of total candle range |
| Bull Signal | Sweeps below CRT low → closes back above + above EMA |
| Bear Signal | Sweeps above CRT high → closes back below + below EMA |
| Cooldown | 10 bars between trades — prevents overtrading |
| EMA Filter | 15-period EMA — confirms trend direction |

---

## Module Responsibilities

| File | Responsibility |
|---|---|
| `app/config.py` | Loads all settings from .env file |
| `app/trader.py` | MT5 connection + trade execution engine |
| `app/main.py` | FastAPI server + webhook endpoint only |
| `run.py` | Single entry point — starts everything |
| `strategies/crt_tbs.pine` | TradingView Pine Script strategy |

---

## Webhook Payload Format

TradingView alert message must be set to:

```json
{
  "action": "{{strategy.order.action}}",
  "comment": "{{strategy.order.comment}}"
}
```

---

## Deployment Environment

| Component | Detail |
|---|---|
| Cloud | AWS EC2 |
| OS | Windows Server |
| Python | 3.12+ |
| Port | 80 (HTTP) |
| Process | Runs continuously — always listening |
