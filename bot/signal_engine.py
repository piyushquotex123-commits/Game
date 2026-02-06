from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta
from enum import Enum
from typing import Iterable


class Direction(str, Enum):
    CALL = "CALL"
    PUT = "PUT"


@dataclass(frozen=True)
class SignalRequest:
    pair: str
    timeframe: str


@dataclass(frozen=True)
class SignalResult:
    pair: str
    timeframe: str
    direction: Direction
    entry_time: datetime
    confidence: float
    reason: str


DEFAULT_PAIRS = [
    "EURUSD",
    "GBPUSD",
    "USDJPY",
    "AUDUSD",
    "USDCAD",
]
DEFAULT_TIMEFRAMES = ["1m", "5m", "15m"]


class SignalEngine:
    """Placeholder signal engine.

    Replace `_score_conditions` and `_select_direction` with your real
    logic using patterns, ML probabilities, and live Deriv candle data.
    """

    def __init__(self, pairs: Iterable[str] | None = None, timeframes: Iterable[str] | None = None) -> None:
        self.pairs = list(pairs) if pairs else DEFAULT_PAIRS
        self.timeframes = list(timeframes) if timeframes else DEFAULT_TIMEFRAMES

    def generate_signal(self, request: SignalRequest) -> SignalResult:
        score = self._score_conditions(request)
        direction = self._select_direction(score)
        entry_time = self._next_candle_time(request.timeframe)
        confidence = min(max(score, 0.0), 1.0)
        reason = "Pattern+probability score met threshold"

        return SignalResult(
            pair=request.pair,
            timeframe=request.timeframe,
            direction=direction,
            entry_time=entry_time,
            confidence=confidence,
            reason=reason,
        )

    def generate_auto_signals(self) -> list[SignalResult]:
        results: list[SignalResult] = []
        for pair in self.pairs:
            for timeframe in self.timeframes:
                request = SignalRequest(pair=pair, timeframe=timeframe)
                result = self.generate_signal(request)
                if result.confidence >= 0.7:
                    results.append(result)
        return results

    def _score_conditions(self, request: SignalRequest) -> float:
        base = 0.55
        if request.timeframe == "1m":
            base += 0.15
        return base

    @staticmethod
    def _select_direction(score: float) -> Direction:
        return Direction.CALL if score >= 0.5 else Direction.PUT

    @staticmethod
    def _next_candle_time(timeframe: str) -> datetime:
        now = datetime.utcnow()
        if timeframe.endswith("m"):
            minutes = int(timeframe[:-1])
            return now + timedelta(minutes=minutes)
        return now + timedelta(minutes=1)
