import discord

from datetime import datetime
from peewee import fn

from bot.entities import Quote as QuoteEntity, BotStats
from bot.datastore.database import Quote as QuoteModel, QuoteMessageLog


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


async def save_quote_log(message: discord.Message, quote: QuoteEntity) -> None:
    message_id: int = message.id
    quote_id: int = quote.id

    QuoteMessageLog.create(message_id=message_id, quote_id=quote_id)


async def get_random_quote(author: discord.Member, guild: discord.Guild) -> QuoteEntity:
    query = QuoteModel.select().order_by(fn.Random())

    if author is not None:
        query = query.filter(QuoteModel.author_id == author.id)

    if guild is not None:
        query = query.filter(QuoteModel.guild_id == guild.id)

    quote: QuoteModel = query.get()

    return QuoteEntity(quote.id, quote.content, quote.author, quote.timestamp)


async def delete_quote(message: discord.Message) -> None:
    message_log = (
        QuoteMessageLog.select().where(QuoteMessageLog.message_id == message.id).get()
    )

    message_log.quote.delete_instance()


async def get_bot_stats() -> BotStats:
    guild_count = QuoteModel.select(QuoteModel.guild_id).distinct().count()

    user_count = QuoteModel.select(QuoteModel.author_id).distinct().count()

    quote_count = QuoteModel.select().count()

    stats: BotStats = BotStats(quote_count, guild_count, user_count)

    return stats
