import discord

from discord.ext import commands

from .entities import Quote, BotStats
from .datastore import (
    get_random_quote,
    save_quote,
    get_bot_stats,
    save_quote_log,
    delete_quote,
)
from .datastore.database import Quote as QuoteModel, QuoteMessageLog

bot = commands.Bot("!")


@bot.command()
async def squote(ctx: commands.Context, author: discord.Member, *quote: str):
    """
    Saves the quote by the @author

    :param author: tag or @ the author
    :param quote: quotes are optional
    """
    quote_combined: str = " ".join(quote)
    invoker: discord.Member = ctx.author
    guild: discord.Guild = ctx.guild

    await save_quote(guild, author, invoker, quote_combined)

    await ctx.message.add_reaction("💯")


@squote.error
async def squote_error(ctx: commands.Context, error):
    """
    Handles parameter errors for `squote`, for example when `author` is an invalid Member
    """
    if isinstance(error, commands.BadArgument):
        await ctx.send("I could not find that member...")


@bot.command()
async def rquote(ctx: commands.Context, author: discord.Member = None):
    """
    Retrieves a random quote [by author, if supplied]

    :param author: [optional] - tag or @ the author
    """
    guild: discord.Guild = ctx.guild

    try:
        quote: Quote = await get_random_quote(author, guild)
    except QuoteModel.DoesNotExist:
        await ctx.send("No quotes in the database!")
    else:
        message = f"{quote.content} - _{quote.author}_, {quote.timestamp.year}"

        res: discord.Message = await ctx.send(message)

        await save_quote_log(res, quote)


@bot.command()
async def quotestats(ctx: commands.Context):
    """
    Display bot stats (e.g. total messages)
    """
    stats: BotStats = await get_bot_stats()

    message = f"**{stats.quote_count}** quotes from **{stats.user_count}** users over **{stats.guild_count}** guilds"

    await ctx.send(message)


async def on_reaction_add(reaction: discord.Reaction, user: discord.Member):
    """
    Delete a quote, when the proper reaction [knife] is applied to a message containing a quote
    """
    if reaction.emoji != "🔪":
        return

    message: discord.Message = reaction.message

    try:
        await delete_quote(message)
    except QuoteMessageLog.DoesNotExist:
        pass
    else:
        await message.channel.send("Message deleted!")


bot.add_listener(on_reaction_add, "on_reaction_add")

bot.help_command
