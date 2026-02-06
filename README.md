# Binary Signal Telegram Bot (Deriv)

This repository contains a Telegram bot starter that generates **binary option signals** using
live market data from the **Deriv API**. It provides:

- **Button-based UI** for all actions
- **Manual signal mode** with pair + timeframe selection
- **Auto mode** that scans all configured pairs/timeframes and posts signals
- **Signal generation engine** that combines technical conditions + probability analysis
- **Extensible strategy framework** (patterns/conditions) for single-candle signals
- **OTC market** placeholders marked as **coming soon**

> ⚠️ This is a starter implementation. The signal engine currently provides a deterministic
> placeholder signal. Replace the scoring logic in `bot/signal_engine.py` with your real
> algorithm (patterns, ML, probability, etc.).

## Quick start

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# edit .env and add TELEGRAM_BOT_TOKEN (never commit real tokens)
python -m bot.main
```

## Configuration

- `TELEGRAM_BOT_TOKEN` – Telegram bot token
- `DERIV_APP_ID` – Deriv app id (optional for demo)

> Never commit real bot tokens. Keep them in `.env` or environment variables.

## Next steps

- Implement live Deriv data fetch + candle normalization.
- Add real strategies/ML scoring.
- Add persistence (signals history, user preferences).
