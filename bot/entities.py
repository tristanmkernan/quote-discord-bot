from dataclasses import dataclass
from datetime import datetime


@dataclass(frozen=True)
class Quote(object):
    content: str
    author: str
    timestamp: datetime
