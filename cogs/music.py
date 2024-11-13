from discord import Embed, FFmpegPCMAudio, PCMVolumeTransformer
from discord.ext import commands
from discord.utils import get
from discord import app_commands
from yt_dlp import YoutubeDL
from asyncio import run_coroutine_threadsafe
import discord
from discord.ui import View, Button

class Music(commands.Cog, name='Music'):
    """
    Music cog for playing audio from YouTube or other sources.
    """
    YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': 'True'}
    FFMPEG_OPTIONS = {
        'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
        'options': '-vn'
    }
    looping = False

    def __init__(self, bot):
        self.bot = bot
        self.song_queue = {}
        self.message = {}

    @staticmethod
    def parse_duration(duration):
        """Convert duration in seconds to H:M:S format."""
        h, m = divmod(duration, 3600)
        m, s = divmod(m, 60)
        return f'{h:d}:{m:02d}:{s:02d}'

    @staticmethod
    def search(author, arg):
        """Search for a song using yt-dlp and return its details."""
        with YoutubeDL(Music.YDL_OPTIONS) as ydl:
            try:
                requests.get(arg)  # Test if arg is a URL
                info = ydl.extract_info(arg, download=False)
            except:
                info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]

            # Extract audio URL
            audio_url = None
            for fmt in info['formats']:
                if fmt.get('acodec') != 'none' and fmt.get('vcodec') == 'none':  # Audio-only format
                    audio_url = fmt['url']
                    break
            if not audio_url:
                raise Exception("No suitable audio format found.")

        embed = (Embed(title='🎵 Now playing:', description=f"[{info['title']}]({info['webpage_url']})", color=0xdbcb34)
                 .add_field(name='Duration', value=Music.parse_duration(info['duration']))
                 .add_field(name='Asked by', value=author)
                 .add_field(name='Uploader', value=f"[{info['uploader']}]({info['channel_url']})")
                 .add_field(name="Queue", value="No queued songs")
                 .add_field(name="Looping", value=Music.looping)
                 .set_thumbnail(url=info['thumbnail']))

        return {'embed': embed, 'source': audio_url, 'title': info['title']}

    async def edit_message(self, ctx):
        """Update the queue message with the current songs."""
        embed = self.song_queue[ctx.guild][0]['embed']
        content = "\n".join([f"({self.song_queue[ctx.guild].index(i)}) {i['title']}" for i in self.song_queue[ctx.guild][1:]]) \
            if len(self.song_queue[ctx.guild]) > 1 else "No more songs in queue..."
        embed.set_field_at(index=3, name="Queue:", value=content, inline=False)
        embed.set_field_at(index=4, name="Looping:", value=Music.looping, inline=False)
        await self.message[ctx.guild].edit(embed=embed)

    def play_next(self, ctx, looping, cutsong):
        """Play the next song in the queue."""
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if not looping:
            if len(self.song_queue[ctx.guild]) > 1:
                del self.song_queue[ctx.guild][0]
                run_coroutine_threadsafe(self.edit_message(ctx), self.bot.loop)
                voice.play(
                    FFmpegPCMAudio(self.song_queue[ctx.guild][0]['source'], **Music.FFMPEG_OPTIONS),
                    after=lambda e: self.play_next(ctx, Music.looping, cutsong=self.song_queue[ctx.guild][0]['source'])
                )
                voice.source = PCMVolumeTransformer(voice.source, volume=1.0)
            else:
                run_coroutine_threadsafe(voice.disconnect(), self.bot.loop)
                run_coroutine_threadsafe(self.message[ctx.guild].delete(), self.bot.loop)
        else:
            voice.play(
                FFmpegPCMAudio(cutsong, **Music.FFMPEG_OPTIONS),
                after=lambda e: self.play_next(ctx, Music.looping, cutsong)
            )
            voice.source = PCMVolumeTransformer(voice.source, volume=1.0)

    @commands.command(aliases=['p'], brief='Play [url/words]', description='Play a video from a URL or search.')
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
            buttonresume = Button(label="Play/Pause", style=discord.ButtonStyle.blurple, emoji="▶️")
            buttonloop = Button(label="LoopSong", style=discord.ButtonStyle.grey, emoji="🎶")
            buttonskip = Button(label="SkipSong", style=discord.ButtonStyle.green, emoji="⏭️")

            async def buttonresume_callback(interaction: discord.Interaction):
                if voice.is_playing():
                    voice.pause()
                    await interaction.response.send_message("⏸️ Paused", ephemeral=True)
                else:
                    voice.resume()
                    await interaction.response.send_message("▶️ Playing", ephemeral=True)

            async def buttonloop_callback(interaction: discord.Interaction):
                Music.looping = not Music.looping
                await interaction.response.send_message(f"Looping: {Music.looping}", ephemeral=True)
                await self.edit_message(ctx)

            async def buttonskip_callback(interaction: discord.Interaction):
                if not Music.looping:
                    voice.stop()
                    await interaction.response.send_message("⏭️ Skipped", ephemeral=True)
                else:
                    await interaction.response.send_message("⏭️ Cannot skip while looping!", ephemeral=True)

            buttonresume.callback = buttonresume_callback
            buttonloop.callback = buttonloop_callback
            buttonskip.callback = buttonskip_callback

            view = View(timeout=None)
            view.add_item(buttonresume)
            view.add_item(buttonloop)
            view.add_item(buttonskip)

            self.song_queue[ctx.guild] = [song]
            self.message[ctx.guild] = await ctx.send(embed=song['embed'], view=view)
            try:
                voice.play(
                    FFmpegPCMAudio(song['source'], **Music.FFMPEG_OPTIONS),
                    after=lambda e: self.play_next(ctx, Music.looping, song['source'])
                )
                voice.source = PCMVolumeTransformer(voice.source, volume=1.0)
            except Exception as e:
                await ctx.send("An error occurred while trying to play the audio.")
        else:
            self.song_queue[ctx.guild].append(song)
            await self.edit_message(ctx)

    @app_commands.command(name="volume", description="Adjust the volume of the song.")
    async def volume(self, interaction: discord.Interaction, volume: float):
        voice = get(self.bot.voice_clients, guild=interaction.guild)
        if voice and voice.is_playing():
            voice.source.volume = volume / 100
            await interaction.response.send_message(f"Volume set to {volume}%", ephemeral=True)
        else:
            await interaction.response.send_message("No audio is playing currently.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Music(bot))
