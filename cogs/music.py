from discord import Embed, FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext import commands
from discord.utils import get
from discord import app_commands

from youtube_dl import YoutubeDL
from asyncio import run_coroutine_threadsafe
import requests
import discord
import discord.ui
from  discord.ui import View, Button, Select

class Music(commands.Cog, name='Music'):
    """
    Can be used by anyone and allows you to listen to music or videos.
    """
    YDL_OPTIONS = {'format': 'bestaudio', 'noplaylist':'True'}
    FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn',}

    def __init__(self, bot):
        self.bot = bot
        self.song_queue = {}
        self.message = {}

    @staticmethod
    def parse_duration(duration):
        result = []
        m, s = divmod(duration, 60)
        h, m = divmod(m, 60)
        return f'{h:d}:{m:02d}:{s:02d}'

    @staticmethod
    def search(author, arg):
        with YoutubeDL(Music.YDL_OPTIONS) as ydl:
            try: requests.get(arg)
            except: info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
            else: info = ydl.extract_info(arg, download=False)

        embed = (Embed(title='🎵 Now playing:', description=f"[{info['title']}]({info['webpage_url']})", color=0xdbcb34)
                .add_field(name='Duration', value=Music.parse_duration(info['duration']))
                .add_field(name='Asked by', value=author)
                .add_field(name='Uploader', value=f"[{info['uploader']}]({info['channel_url']})")
                .add_field(name="Queue", value=f"No queued musics")
                .set_thumbnail(url=info['thumbnail']))

        return {'embed': embed, 'source': info['formats'][0]['url'], 'title': info['title']}

    async def edit_message(self, ctx):
        embed = self.song_queue[ctx.guild][0]['embed']
        content = "\n".join([f"({self.song_queue[ctx.guild].index(i)}) {i['title']}" for i in self.song_queue[ctx.guild][1:]]) if len(self.song_queue[ctx.guild]) > 1 else "No more songs in queue..."
        embed.set_field_at(index=3, name="Queue:", value=content, inline=False)
        await self.message[ctx.guild].edit(embed=embed)

    def play_next(self, ctx):
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if len(self.song_queue[ctx.guild]) > 1:
            del self.song_queue[ctx.guild][0]
            run_coroutine_threadsafe(self.edit_message(ctx), self.bot.loop)
            voice.play(FFmpegPCMAudio(self.song_queue[ctx.guild][0]['source'], **Music.FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx))
            voice.source = PCMVolumeTransformer(voice.source, volume=1.0)
            voice.is_playing()
        else:
            run_coroutine_threadsafe(voice.disconnect(), self.bot.loop)
            run_coroutine_threadsafe(self.message[ctx.guild].delete(), self.bot.loop)

    @commands.command(aliases=['p'], brief='Du play [url/words]', description='Listen to a video from an url or from a youtube search')
    async def play(self, ctx, *, video: str):
        channel = ctx.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        song = Music.search(ctx.author.mention, video)

        if voice and voice.is_connected():
            await voice.move_to(channel)
        else:
            voice = await channel.connect()     

        await ctx.message.delete()
        
        if not voice.is_playing():

#-------------------------------------------------------------------------------------------------
            async def buttonresume_callback(interaction: discord.Interaction):
                await interaction.response.send_message("⏯️ Resumed", ephemeral=True, delete_after=10)
                voice.resume()

            async def buttonpause_callback(interaction: discord.Interaction):
                await interaction.response.send_message("⏸️ Paused", ephemeral=True, delete_after=10)
                voice.pause()

            async def buttonqueue_callback(interaction: discord.Interaction):
                await interaction.response.send_message("🎶 Queued", ephemeral=True, delete_after=10)
                self.song_queue[ctx.guild].append(song)
                await self.edit_message(ctx)
            
            async def buttonskip_callback(interaction: discord.Interaction):
                await interaction.response.send_message("⏭️ Skipped", ephemeral=True, delete_after=10)
                voice.stop()
                          
#-------------------------------------------------------------------------------------------------
            buttonresume = Button(label="ResumeSong", style=discord.ButtonStyle.blurple, emoji="▶️")
            buttonresume.callback = buttonresume_callback

            buttonpause = Button(label="PauseSong", style=discord.ButtonStyle.red, emoji="⏸️")
            buttonpause.callback = buttonpause_callback

            buttonqueue = Button(label="QueueSong", style=discord.ButtonStyle.grey, emoji="🎶")
            buttonqueue.callback = buttonqueue_callback
            
            buttonskip = Button(label="SkipSong", style=discord.ButtonStyle.green, emoji="⏭️")
            buttonskip.callback = buttonskip_callback

            view = View(timeout=None)
            view.add_item(buttonresume)
            view.add_item(buttonpause)
            view.add_item(buttonqueue)
            view.add_item(buttonskip)
#-------------------------------------------------------------------------------------------------

            self.song_queue[ctx.guild] = [song]
            self.message[ctx.guild] = await ctx.send(embed=song['embed'], view=view)
            voice.play(FFmpegPCMAudio(song['source'], **Music.FFMPEG_OPTIONS), after=lambda e: self.play_next(ctx))
            voice.source = PCMVolumeTransformer(voice.source, volume=1.0)
            voice.is_playing()
        else:
            self.song_queue[ctx.guild].append(song)
            await self.edit_message(ctx)
#-------------------------------------------------------------------------------------------------
 
    @app_commands.command(name="volume", description="adjust the volume of song")
    async def volume(self, interaction: discord.Interaction, volume: float):
        voice = get(self.bot.voice_clients, guild=interaction.guild)
        new_volume = volume/100                   
        voice.source.volume = new_volume
        await interaction.response.send_message(f"Volume: {volume}", ephemeral=True, delete_after=10)


async def setup(bot):
    await bot.add_cog(Music(bot))
