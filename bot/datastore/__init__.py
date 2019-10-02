import discord

from datetime import datetime
from functools import singledispatch
from peewee import fn

from bot.entities import Quote as QuoteEntity
from bot.datastore.database import Quote as QuoteModel


async def save_quote(
    guild: discord.Guild, author: discord.Member, invoker: discord.Member, content: str
) -> None:
    guild_id: int = guild.id
    author_name: str = author.nick or author.display_name
    author_id: int = author.id
    invoker_name: str = invoker.nick or invoker.display_name
    invoker_id: int = invoker.id

    QuoteModel.create(
        guild_id=guild.id,
        content=content,
        author=author_name,
        author_id=author_id,
        invoker=invoker_name,
        invoker_id=invoker_id,
        # TODO enforce solid datetime rules
        timestamp=datetime.utcnow(),
    )


@singledispatch
async def get_random_quote(_) -> QuoteEntity:
    quote: QuoteModel = QuoteModel.select().order_by(fn.Random()).get()
    return QuoteEntity(quote.content, quote.author, quote.timestamp)


@get_random_quote.register
async def _(author: discord.Member) -> QuoteEntity:
    quote: QuoteModel = QuoteModel.select().filter(
        QuoteModel.author_id == author.id
    ).order_by(fn.Random()).get()
    return QuoteEntity(quote.content, quote.author, quote.timestamp)
