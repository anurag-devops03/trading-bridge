# CRT Trading Bridge — Automated Trading Infrastructure

A production-grade automated trading bridge that connects TradingView alerts
to MetaTrader 5 (MT5) for live trade execution on GOLD (XAUUSD), deployed on AWS EC2.

## Tech Stack
- **Strategy:** Pine Script v6 (TradingView)
- **Bridge:** Python 3.12 + FastAPI
- **Broker API:** MetaTrader5 (MT5)
- **Web Server:** Uvicorn
- **Hosting:** AWS EC2 (Windows Server)
- **Security:** python-dotenv (.env based credentials)

## System Architecture
TradingView (Pine Script Strategy)
│
│  Webhook Alert (HTTP POST)
▼
Python FastAPI Bridge (AWS EC2)
│
│  MT5 Python Library
▼
MetaTrader 5 Terminal
│
▼
Live Trade Executed (GOLD)

## Project Status
- [x] Phase 1 — Project Structure
- [x] Phase 2 — Security Setup (.gitignore + .env)
- [ ] Phase 3 — Clean Modular Codebase
- [ ] Phase 4 — Dependencies (requirements.txt)
- [ ] Phase 5 — Documentation
- [ ] Phase 6 — GitHub Deployment

## Quick Start

### Prerequisites
- Python 3.10+
- MetaTrader 5 Terminal (Windows)
- Git

### Run Locally
```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/trading-bridge.git
cd trading-bridge

# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Setup environment variables
cp .env.example .env
nano .env  # Fill in your MT5 credentials

# Start the bridge
python run.py
```

### Webhook Endpoint
| Method | Endpoint   | Description                        |
|--------|------------|------------------------------------|
| GET    | /          | Health check — bridge status       |
| POST   | /webhook   | Receives TradingView alert payload |

### TradingView Alert Payload Format
```json
{
  "action": "buy",
  "comment": "Long Entry new"
}
```
