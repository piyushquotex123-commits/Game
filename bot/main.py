from __future__ import annotations

import logging
import os
from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CallbackQueryHandler, CommandHandler, ContextTypes

from bot.signal_engine import DEFAULT_PAIRS, DEFAULT_TIMEFRAMES, SignalEngine, SignalRequest

load_dotenv()

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

ENGINE = SignalEngine()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [InlineKeyboardButton("Manual Signal", callback_data="manual")],
        [InlineKeyboardButton("Auto Mode", callback_data="auto")],
        [InlineKeyboardButton("Settings", callback_data="settings")],
        [InlineKeyboardButton("Help", callback_data="help")],
    ]
    await update.message.reply_text(
        "Binary Signal Bot\n\nChoose a mode:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )


async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "manual":
        await show_pairs(query)
    elif query.data == "auto":
        await run_auto_mode(query)
    elif query.data == "settings":
        await query.edit_message_text("Settings coming soon.")
    elif query.data == "help":
        await query.edit_message_text(
            "Use Manual Signal to pick a pair and timeframe.\n"
            "Use Auto Mode to scan all pairs/timeframes.\n"
            "OTC markets: coming soon."
        )
    elif query.data.startswith("pair:"):
        pair = query.data.split(":", 1)[1]
        context.user_data["pair"] = pair
        await show_timeframes(query)
    elif query.data.startswith("tf:"):
        timeframe = query.data.split(":", 1)[1]
        pair = context.user_data.get("pair")
        if not pair:
            await show_pairs(query)
            return
        await run_manual_signal(query, pair, timeframe)


async def show_pairs(query) -> None:
    keyboard = [[InlineKeyboardButton(pair, callback_data=f"pair:{pair}")] for pair in DEFAULT_PAIRS]
    keyboard.append([InlineKeyboardButton("Back", callback_data="help")])
    await query.edit_message_text(
        "Select a pair:", reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def show_timeframes(query) -> None:
    keyboard = [[InlineKeyboardButton(tf, callback_data=f"tf:{tf}")] for tf in DEFAULT_TIMEFRAMES]
    keyboard.append([InlineKeyboardButton("Back", callback_data="manual")])
    await query.edit_message_text(
        "Select a timeframe:", reply_markup=InlineKeyboardMarkup(keyboard)
    )


async def run_manual_signal(query, pair: str, timeframe: str) -> None:
    request = SignalRequest(pair=pair, timeframe=timeframe)
    signal = ENGINE.generate_signal(request)
    await query.edit_message_text(
        "Manual Signal\n"
        f"Pair: {signal.pair}\n"
        f"Timeframe: {signal.timeframe}\n"
        f"Direction: {signal.direction}\n"
        f"Entry Time (UTC): {signal.entry_time:%H:%M:%S}\n"
        f"Confidence: {signal.confidence:.0%}\n"
        f"Reason: {signal.reason}"
    )


async def run_auto_mode(query) -> None:
    signals = ENGINE.generate_auto_signals()
    if not signals:
        await query.edit_message_text("Auto Mode: No signals met criteria.")
        return

    lines = [
        "Auto Mode Signals:",
    ]
    for signal in signals:
        lines.append(
            f"{signal.pair} {signal.timeframe} {signal.direction}"
            f" @ {signal.entry_time:%H:%M:%S} ({signal.confidence:.0%})"
        )
    await query.edit_message_text("\n".join(lines))


def main() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise RuntimeError("Missing TELEGRAM_BOT_TOKEN")

    application = Application.builder().token(token).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_callback))

    LOGGER.info("Bot started")
    application.run_polling()


if __name__ == "__main__":
    main()
