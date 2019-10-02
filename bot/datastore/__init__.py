import discord

from datetime import datetime
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
        guild_id=guild_id,
        content=content,
        author=author_name,
        author_id=author_id,
        invoker=invoker_name,
        invoker_id=invoker_id,
        timestamp=datetime.utcnow(),
    )


async def get_random_quote(author: discord.Member, guild: discord.Guild) -> QuoteEntity:
    query = QuoteModel.select().order_by(fn.Random())

    if author is not None:
        query = query.filter(QuoteModel.author_id == author.id)

    if guild is not None:
        query = query.filter(QuoteModel.guild_id == guild.id)

    quote: QuoteModel = query.get()

    return QuoteEntity(quote.content, quote.author, quote.timestamp)
