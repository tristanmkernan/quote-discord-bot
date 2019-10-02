from peewee import fn

from bot.entities import Quote as QuoteEntity

from .database import Quote as QuoteModel


async def save_quote(content: str) -> None:
    quote = QuoteModel.create(content=content)


async def get_random_quote() -> QuoteEntity:
    quote = QuoteModel.select().order_by(fn.Random()).get()
    return QuoteEntity(quote.content)
