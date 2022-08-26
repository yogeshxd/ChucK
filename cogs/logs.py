from discord import Embed, Colour
from discord.ext import commands
from discord.utils import get

from datetime import datetime, timezone
from sqlite3 import connect
import random



class Logs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @staticmethod
    def create_embed(title=None, description=None , color=None, timestamp=None):
        embed = Embed(
            title=title,
            description=description,
            color=color,
            timestamp=timestamp
        )
        return embed

    @staticmethod
    def get_data(guild_id):
        with connect('data.db') as conn:
            c = conn.cursor()
            c.execute("SELECT * FROM logs WHERE ID=?", (guild_id,))
            return c.fetchone()

    @commands.command(hidden=True)
    @commands.has_permissions(administrator=True)
    async def logs(self, ctx):
        await ctx.message.delete()
        state = Logs.get_data(ctx.guild.id)
        with connect('data.db') as conn:
            c = conn.cursor()
            if state == None:
                c.execute("INSERT INTO logs(ID, State) VALUES(?, ?)", (ctx.guild.id, 1))
            elif state == (ctx.guild.id, 0):
                c.execute("UPDATE logs SET State=? WHERE ID=?", (1, ctx.guild.id))
            else:
                c.execute("UPDATE logs SET State=? WHERE ID=?", (0, ctx.guild.id))
            conn.commit()
            state = 'enabled' if state==(ctx.guild.id, 0) else 'disabled'
            await ctx.send(f"Logs {state}", delete_after=5.0)

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        param = error.param.name if isinstance(error, commands.MissingRequiredArgument) else ''
        perms = ', '.join(error.missing_perms) if isinstance(error, commands.BotMissingPermissions) else ''
        invoke_errors = {
            'index': "Index error!",
            'is_playing': "I'm not connected to any channel!",
            'unpack': "User has no warns !",
            'channel': "You're not connected to any channel!",
            'Missing Permissions': "I'm not allowed to do this!",
            'ValueError': 'Wrong arguments!',
            'KeyError': 'Wrong arguments!'
        }
        errors = {
            "<class 'discord.ext.commands.errors.MissingRequiredArgument'>": f'You forgot an argument: {param}',
            "<class 'discord.ext.commands.errors.CommandNotFound'>": 'Command not found!',
            "<class 'discord.ext.commands.errors.MissingPermissions'>": "You can't use this command!",
            "<class 'discord.ext.commands.errors.BotMissingPermissions'>": f'I need the following perms to do this: {perms} !',
            "<class 'discord.ext.commands.errors.BadArgument'>": 'You must input an integer!' if 'int' in str(error) else "Membre introuvable !",
            "<class 'discord.ext.commands.errors.CommandInvokeError'>": ''.join([value for key, value in invoke_errors.items() if key in str(error)]),
        }
        clean_error = errors[str(type(error))]
        if not clean_error:
            raise error
        embed = Embed(title="❌ Something went wrong:", description=clean_error, color=0xe74c3c)
        await ctx.message.delete()
        await ctx.send(embed=embed, delete_after=5.0)

    @commands.Cog.listener()
    async def on_command_completion(self, ctx):
        state = Logs.get_data(ctx.guild.id)
        if state == None or (ctx.command.name!='logs' and state==(ctx.guild.id, 0)):
            return

        channel = get(ctx.guild.text_channels, name='logs')
        state = 'enabled' if state==(ctx.guild.id, 1) else 'disabled'

        cmd = ctx.command.name
        cmd_args = ctx.message.content[len(cmd)+1:].split()
        if len(cmd_args)<2:
            cmd_args += ['', '']
        cmd_list = {
            'ban': {'title:': ':man_judge: User banned', 'desc': f"{ctx.author.mention} banned {cmd_args[0]}\n**Reason:** {' '.join(cmd_args[1:])}", 'color': 0xe74c3c},
            'unban': {'title': ':man_judge: User unbanned', 'desc': f"{ctx.author.mention} unbanned {cmd_args[0]}\n**Reason:** {' '.join(cmd_args[1:])}", 'color': 0xc27c0e},
            'kick': {'title': ':man_judge: User kicked', 'desc': f"{ctx.author.mention} kicked {cmd_args[0]}\n**Reason:** {' '.join(cmd_args[1:])}", 'color': 0xe74c3c},
            'warn': {'title': ':warning: User warned', 'desc':f"{ctx.author.mention} warned {cmd_args[0]}\n**Reason:** {' '.join(cmd_args[1:])}", 'color': 0xe67e22},
            'mute': {'title': ':mute: User muted', 'desc': f"{ctx.author.mention} muted {cmd_args[0]}\n**Duration**: {cmd_args[1]}\n**Reason:** {' '.join(cmd_args[2:])}", 'color': 0xe74c3c},
            'clear': {'title': ':wastebasket:  Messages deleted', 'desc': f"{ctx.author.mention} deleted some messages.", 'color': 0x1f8b4c},
            'poll': {'title': ':clipboard: Poll created', 'desc': f"Question: *{cmd_args[0]}*\nChoices: *{' / '.join(cmd_args[1:])}*\nBy {ctx.author.mention}",'color': 0x7289da},
            'logs': {'title': f':printer: Logs {state}', 'desc': f'{ctx.author.mention} {state} logs', 'color': 0x11806a},
        }

        if not cmd in cmd_list.keys():
            return

        embed = Logs.create_embed(cmd_list[cmd]['title'], cmd_list[cmd]['desc'], cmd_list[cmd]['color'], datetime.now())
        await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_remove(self, member):
        channel = get(member.guild.text_channels, name='logs')
        embed = Logs.create_embed(None, f'**:outbox_tray: {member.mention} left the server**', 0xe74c3c, datetime.now())
        await channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_member_join(self, member):
        state = Logs.get_data(member.guild.id)
        if state == None or state == (member.guild.id, 0): return

        channel = get(member.guild.text_channels, name='logs')
        embed = Logs.create_embed(None, f'**:inbox_tray: {member.mention} joined the server**', 0x2ecc71, datetime.now())
        await channel.send(embed=embed)

        wel = ['Welcome Welcome Buddy','Hope you bought pizzas','that was a fucking wild entry',
        'just landed','hoped into the server','Welcome!! Party is still on','let\'s start party now',
        'you are most welcome'
        ]
        embed = Logs.create_embed(":inbox_tray: New member !", f'{member.mention} {random.choice(wel)}.', 0x2ecc71, datetime.now())
        embed.set_image(url=member.avatar_url)
        await member.guild.system_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        state = Logs.get_data(before.guild.id)
        if state == None or state == (before.guild.id, 0): return

        entry = await after.guild.audit_logs(limit=1).flatten()
        channel = get(before.guild.text_channels, name='logs')
        embed = Logs.create_embed(":notepad_spiral: Member modification", f'{entry[0].user.mention} changed {before.mention}', 0x99aab5, datetime.now())

        if before.display_name != after.display_name:
            embed.add_field(name="Nickname:", value=f"{before.display_name} → {after.display_name}")
        elif before.roles != after.roles:
            new_roles = [role.name for role in after.roles if role not in before.roles]
            removed_roles = [role.name for role in before.roles if role not in after.roles]
            new_roles = "New roles: "+("".join(new_roles) if new_roles else "None")
            removed_roles = "Removed roles: "+("".join(removed_roles) if removed_roles else "None")
            embed.add_field(name="Roles:", value=f"{new_roles}\n{removed_roles}")
        else:
            return
        await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        with connect('data.db') as conn:
            c = conn.cursor()
            c.execute("INSERT INTO logs (ID, State) VALUES (?, ?)", (guild.id, 0))
            c.execute(f'CREATE TABLE IF NOT EXISTS "{guild.id}" (User_ID INTEGER, Premium INTEGER)')
            conn.commit()
        await channel.send(embed=embed)


async def setup(bot):
    await bot.add_cog(Logs(bot))
