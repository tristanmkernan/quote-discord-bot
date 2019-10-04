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


@squote.error
async def squote_error(ctx: commands.Context, error):
    if isinstance(error, commands.BadArgument):
        await ctx.send("I could not find that member...")


@bot.command()
async def rquote(ctx: commands.Context, author: discord.Member = None):
    """
    Retrieves a random quote [by author, if supplied]
    """
    guild: discord.Guild = ctx.guild
    quote: Quote = await get_random_quote(author, guild)

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


@bot.command()
async def quotehelp(ctx: commands.Context):
    """
    TODO
    https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.HelpCommand
    """


async def on_reaction(reaction: discord.Reaction, user: discord.Member):
    """
    Delete a quote, when the proper reaction [knife] is applied to a previous message by the bot
    """
    if reaction.emoji != "🔪":
        return

    message: discord.Message = reaction.message

    await delete_quote(message)

    await message.channel.send("Message deleted!")


bot.add_listener(on_reaction, "on_reaction_add")
