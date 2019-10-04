from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Quote(object):
    content: str
    author: str
    timestamp: datetime


@dataclass(frozen=True)
class BotStats(object):
    quote_count: int
    guild_count: int
    user_count: int
