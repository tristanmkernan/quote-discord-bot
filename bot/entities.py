from dataclasses import dataclass


@dataclass(frozen=True)
class Quote(object):
    content: str
