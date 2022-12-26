import interactions
import config

bot = interactions.Client(token=config.token)

@bot.command(
    name="test",
    description="Yess",
)
async def my_first_command(ctx: interactions.CommandContext):
    await ctx.send("It's freaking workingggg!!!!!!!")

bot.start()
