import discord

from discord.ext import commands

from .entities import Quote, BotStats
from .datastore import get_random_quote, save_quote, get_bot_stats

bot = commands.Bot("!")


@bot.command()
async def squote(ctx: commands.Context, author: discord.Member, *quote: str):
    """
    Saves the given quote
    """
    quote_combined: str = " ".join(quote)
    invoker: discord.Member = ctx.author
    guild: discord.Guild = ctx.guild

    await save_quote(guild, author, invoker, quote_combined)

    await ctx.message.add_reaction("💯")


@bot.command()
async def rquote(ctx: commands.Context, author: discord.Member = None):
    """
    Retrieves a random quote [by author, if supplied]
    """
    guild: discord.Guild = ctx.guild
    quote: Quote = await get_random_quote(author, guild)

    message = f"{quote.content} - _{quote.author}_, {quote.timestamp.year}"

    await ctx.send(message)


@bot.command()
async def quotestats(ctx: commands.Context):
    """
    Display bot stats (e.g. total messages)
    """
    stats: BotStats = await get_bot_stats()

    message = f"_{stats.quote_count} quotes from {stats.user_count} users over {stats.guild_count} guilds_"

    await ctx.send(message)
