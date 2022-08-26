from discord import Embed, Color
from discord.ext import commands
from discord.utils import get as dget
import random

from requests import get, post
from os import environ

class Chat(commands.Cog, name='Chat'):
    """
    Can be used by everyone and gathers every non specific commands.
    """
    def __init__(self, bot):
        self.bot = bot

    # @commands.command(brief='Du help [category]', description='Show this message')
    # async def help(self, ctx, category: str = None):
    #     embed = Embed(color=0x3498db)
    #     embed.title = '📋 Category list:' if not category else f'ℹ️ About the {category} category:'
    #     await ctx.message.delete()
    #     if not category:
    #         for cat in self.bot.cogs:
    #             if cat in ['Test', 'Logs']:
    #                 pass
    #             else:
    #                 cog = self.bot.get_cog(cat)
    #                 embed.add_field(name=cat, value=f"{cog.description}\nType `Du help {cat}` for more informations.", inline=False)
    #     else:
    #         for cmd in self.bot.get_cog(category.capitalize()).get_commands():
    #             if cmd.hidden:
    #                 pass
    #             else:
    #                 embed.add_field(name=f"Du {cmd.name}", value=f"{cmd.description} (`{cmd.brief}`)", inline=False)
    #     await ctx.send(embed=embed)

    @commands.command(hidden=True)
    async def rules(self, ctx):
        rules = {
            '👍 Rule n°1': "Respect eachother! For a nice and kind chat, don't swear or be mean.",
            '🗳️ Rule n°2': "This server is dedicated to Hazard Wizard. That means no political or religious topics, racism, harassment or offensive content.",
            '🔕 Rule n°3': "Don't spam and don't abuse mentions. We want clear and understandable chats, not a weird mess.",
            '👦 Rule n°4': "Use an appropriate nickname and avatar. Keep it family-friendly.",
            '🔒 Rule n°5': "Don't share personnal informations! Protect your privacy and other's privacy.",
            '💛 Rule n°6': "Use your common sense. Don't start fighting on some common shits.",
            '💬 Rule n°7': "Self-promotions is forbidden! You can only share your content in #promotions.",
            '🙏 Rule n°8': "Don't beg for roles/permissions. It's just annoying and you'll never get roles by begging.",
            '📑 Rule n°9': "Follow [Discord Community Guidelines](https://discord.com/guidelines) and [Terms Of Service](https://discord.com/terms).",
        }
        embed = Embed(title="📃 Server's rules:", color=0xa84300)
        embed.set_footer(text="Click ✔️ to access the server")
        for key, value in rules.items():
            embed.add_field(name=key, value=f"{value}\n", inline=False)
        await ctx.message.delete()
        msg = await ctx.send(embed=embed)
        await msg.add_reaction('✅')

    @commands.command(brief='Du poll "[question]" [choices]', description='Create a poll (9 maximum choices)')
    async def poll(self, ctx, *items):
        question = items[0]
        answers = '\n'.join(items[1:])
        embed = Embed(title='New poll:', description=f":grey_question: __{question}__", color=0x3498db)
        await ctx.message.delete()
        for i in range(1, len(items)):
            embed.add_field(name=f"Option n°{i}", value=items[i], inline=False)
        embed.set_footer(text=f"Asked by: {ctx.author}")
        message = await ctx.channel.send(embed=embed)
        reactions = ['1️⃣','2️⃣','3️⃣','4️⃣','5️⃣','6️⃣','7️⃣','8️⃣','9️⃣']

        for i in range(len(items[1:])):
            await message.add_reaction(reactions[i])

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        member = payload.member
        if payload.emoji.name == '✅' and not member.bot:
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id) 
            reaction = dget(message.reactions, emoji=payload.emoji.name)
            role = dget(member.guild.roles, name='Member')
            if not role in member.roles:
                await member.add_roles(role)
            else:
                pass
            await reaction.remove(member)

    @commands.command(brief="Du hii", description='Replies with random msg.')
    async def hii(self, ctx):
        l1 = [
        'Heyy yaa wassup!','Hello Buddy','Heyyaa!','wassup man!! how\'re u doing','Give me nitro or I\'m not gonna talk with u.',
        'Puck Off! I\'m not in mood to talk.','Ohhhh! Not you again','Wassup kiddo','Suprabhat Bhosdiwale','I want charas right NOW!!!',
        'Charas Ganja Mereko Pyara','Nooooo!!! Not you again...','PUCCCKKKK OFFF You Little Pig','Heyy Piggy Poggy','Hello lavieth the pretensious asshole',
        'Pucker Pucker You are a Pucker','Orr lodu kaisa??','Lo chutiya is back','or gandu maze me??','Nikal laude','Bhag Bhosdike','Are maa chudi padi hai',
        'East or west your bhosda is best','mausi chi gand','Oh my GOOOD, You remember me.','Love you mannnn','You are talking to a bot. Go get some life..',
        'Really mannnn, You are this lonely??','Ohhhh finally you got the time to talk to me','Ohhh finally, I was dying to talk to you','Heyy buddy, How\'s you doing'
        ]
        await ctx.channel.send(random.choice(l1))

    @commands.command(brief="Du invite", description='Invite bot to your server...')
    async def invite(self, ctx):
        msg = 'To invite me to your server [click here](https://discord.com/api/oauth2/authorize?client_id=748044205242187886&permissions=8&scope=bot)...'
        embed = Embed(title='Invite Chuck:',description=msg, color=random.randint(0, 0xffffff))
        se = await ctx.send(embed=embed)
        

async def setup(bot):
    await bot.add_cog(Chat(bot))