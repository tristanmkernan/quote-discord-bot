from discord.ext import commands

from .entities import Quote
from .datastore import get_random_quote, save_quote

bot = commands.Bot("!")


@bot.command()
async def squote(ctx, quote: str):
    """
    Saves the given quote
    """
    await save_quote(quote)

    await ctx.message.add_reaction("💯")


@bot.command()
async def rquote(ctx):
    """
    Retrieves a random quote
    """
    quote: Quote = await get_random_quote()
    await ctx.send(quote.content)
