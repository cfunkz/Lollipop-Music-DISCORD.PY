import discord
from discord.ext import commands
import wavelink
from discord import Embed
from view import PlaylistView, PlaylistPlayingView, PlayingView
import asyncio



class MusicCommands(commands.Cog):
  def __init__(self, bot):
      self.bot = bot

  async def create_progress_bar(self, current, total, length=20):
    progress = int((current / total) * length)
    bar = "▬" * progress + "🔘" + "▬" * (length - progress)
    return bar

  async def format_time(self, seconds):
    minutes, seconds = divmod(seconds, 60)
    return f"{int(minutes)} minutes and {int(seconds)} seconds"

  async def create_now_playing_embed(self, ctx, track):
    try:
        player: wavelink.Player = ctx.guild.voice_client
        volume = player.volume
        duration_in_seconds = track.length / 1000  # Convert milliseconds to seconds
        current_time = player.position / 1000  # Convert milliseconds to seconds
        time_left_str = await self.format_time(duration_in_seconds - current_time)
        progress_bar = await self.create_progress_bar(current_time, duration_in_seconds)
        embed = Embed(title="🎶 Now playing", description=f"`{track.title}`", color=discord.Color.blue())
        embed.set_image(url=track.thumb)
        embed.add_field(name="Progress", value=progress_bar, inline=False)
        embed.add_field(name="Time Left", value=time_left_str, inline=False)
        embed.add_field(name="Volume:", value=f"`{volume}/100`", inline=False)
        embed.set_footer(text=f"{len(player.queue)} songs in queue.")
        return embed
    except:
        await ctx.send("Error making embed!")

  async def update_now_playing(self, ctx, message):
    player: wavelink.Player = ctx.guild.voice_client
    while player and player.is_playing():
        curr_track = player.current
        embed = await self.create_now_playing_embed(ctx, curr_track)
        await message.edit(embed=embed)  # Edit the existing message
        await asyncio.sleep(5)  # Update every 5 seconds

  @commands.guild_only()
  @commands.hybrid_command(name="play")
  async def _play(self, ctx, *, query):
      channel = ctx.author.voice.channel
      tracks: list[wavelink.YouTubeTrack] = await wavelink.YouTubeTrack.search(query)
      player: wavelink.Player = ctx.guild.voice_client
      if not player:
          player: wavelink.Player = await channel.connect(cls=wavelink.Player)
          player.autoplay = True
          if "list" in query:
              playlist = await wavelink.YouTubePlaylist.convert(ctx, query)
              embed = Embed(title="⚠️ Warning!", description=f"Do you want to add \n`{playlist.tracks[0].title}`\n\n**Or**\n\n`{len(playlist.tracks)}` songs to the queue?")
              await ctx.send(embed=embed, view=PlaylistView(ctx, player, playlist))
          else:
              await player.play(tracks[0])
              await asyncio.sleep(1)
              curr_track = player.current
              embed = await self.create_now_playing_embed(ctx, curr_track)
              message = await ctx.send(embed=embed, view=PlayingView(ctx, player))
                # Call the function to update the message
              await self.update_now_playing(ctx, message)
      else:
          if "list" in query:
              playlist = await wavelink.YouTubePlaylist.convert(ctx, query)
              embed = Embed(title="⚠️ Warning!", description=f"Do you want to add \n\n`{playlist.tracks[0].title}`\n\n**Or**\n\n`{len(playlist.tracks)}` songs to the queue?",color=discord.Color.blue())
              embed.set_footer(text=f"{len(player.queue)} songs in the queue.")
              embed.set_thumbnail(url=playlist.tracks[0].thumb)
              await ctx.send(embed=embed, view=PlaylistPlayingView(ctx, player, playlist))
          else:
              player.queue(tracks[0])
              embed = Embed(title="➕ Added to queue", description=f"`{tracks[0].title}`", color=discord.Color.blue())
              embed.set_footer(text=f"{len(player.queue)} songs in the queue.")
              embed.set_thumbnail(url=tracks[0].thumb)
              await ctx.send(embed=embed)
            
  @commands.guild_only()
  @commands.hybrid_command(name="nowplaying")
  async def nowplaying(self, ctx):
      player: wavelink.Player = ctx.guild.voice_client
      if player and player.is_playing:
          # Send the initial message
          curr_track = player.current
          embed = await self.create_now_playing_embed(ctx, curr_track)
          message = await ctx.send(embed=embed, view=PlayingView(ctx, player))
          # Call the function to update the message
          await self.update_now_playing(ctx, message)
      else:
          await ctx.send('Nothing is currently playing.')
        
  @commands.guild_only()
  @commands.hybrid_command(name="skip")
  async def _skip(self, ctx):
      player: wavelink.Player = ctx.guild.voice_client
      if player and player.is_playing():
          await player.stop(force=True)
          await ctx.send("Skipped the current song.")
      else:
          await ctx.send("Nothing is currently playing.")
        
  @commands.guild_only()
  @commands.hybrid_command(name="previous")
  async def _previous(self, ctx):
      player: wavelink.Player = ctx.guild.voice_client
      if player and len(player.queue.history) > 0:
          prev_track = player.queue.history[-2]  # Get the last song in the history
          await player.play(prev_track)
          await ctx.send(f"Playing previous track: `{prev_track.title}`")
      else:
          await ctx.send("No previous track to play.")
        
  @commands.guild_only()
  @commands.hybrid_command(name="clear")
  async def _clearqueue(self, ctx):
    player: wavelink.Player = ctx.guild.voice_client
    if player:
        player.queue.reset()
        await ctx.send("Queue cleared!")
    else:
        await ctx.send("No queue to clear!")
      
  @commands.guild_only()
  @commands.hybrid_command(name="shuffle")
  async def _shuffle(self, ctx):
      player: wavelink.Player = ctx.guild.voice_client
      if player:
        player.queue.shuffle()
        await ctx.send("Queue Shuffled")
      else:
        return await ctx.send("The bot is disconnected.")
        
  @commands.guild_only()
  @commands.hybrid_command(name="pause")
  async def _pause(self, ctx):
      player: wavelink.Player = ctx.guild.voice_client
      if player:
        await player.pause()
        await ctx.send("Paused")
      else:
        return await ctx.send("The bot is disconnected.")
        
  @commands.guild_only()
  @commands.hybrid_command(name="resume")
  async def _resume(self, ctx):
      player: wavelink.Player = ctx.guild.voice_client
      if player:
        await player.resume()
        await ctx.send("Resumed.")
      else:
        return await ctx.send("The bot is disconnected.")
        
  @commands.guild_only()
  @commands.hybrid_command(name="stop")
  async def _disconnect(self, ctx):
      player: wavelink.Player = ctx.guild.voice_client
      if player:
        await player.disconnect()
        await ctx.send("```Disconnected```")
      else:
        return await ctx.send("The bot not connected.")
        
  @commands.guild_only()
  @commands.hybrid_command(name="volume")
  async def _vol(self, ctx, volume: int):
      player: wavelink.Player = ctx.guild.voice_client
      if volume > 100:
          return await ctx.send("100% Is Max")
      elif volume < 0:
          return await ctx.send("0% Is Lowest")
      await player.set_volume(volume)
      await ctx.send(f"```Volume set to %{volume}```")

  @commands.guild_only()
  @commands.hybrid_command(name="repeatall")
  async def _loopall(self, ctx):
      player: wavelink.Player = ctx.guild.voice_client
      if player:
        if player.queue.loop_all == True:
            player.queue.loop_all = False
            await ctx.send("Repeat all off.")
        else:
            player.queue.loop_all = True
            await ctx.send("Repeat all on.")
      else:
        await ctx.send(f"No player connected.")

  @commands.guild_only()
  @commands.hybrid_command(name="repeat")
  async def _loop(self, ctx):
      player: wavelink.Player = ctx.guild.voice_client
      if player:
        if player.queue.loop == True:
            player.queue.loop = False
            await ctx.send("Repeat off.")
        else:
            player.queue.loop = True
            await ctx.send("Repeat on.")
      else:
        await ctx.send(f"No player connected.") 


async def setup(bot):
    cog = MusicCommands(bot)
    await bot.add_cog(cog)