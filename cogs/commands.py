import discord
from discord.ext import commands
import wavelink
from discord import Embed
from view import PlaylistView, PlaylistPlayingView, PlayingView, InviteButton
import asyncio
import time

class MusicCommands(commands.Cog):
  def __init__(self, bot):
      self.bot = bot

  async def format_time(self, seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    if hours > 0:
        return f"`{int(hours)}:{int(minutes)}:{int(seconds)}`"
    else:
        return f"`{int(minutes)}:{int(seconds)}`"

  async def create_now_playing_embed(self, ctx, track):
    try:
        player: wavelink.Player = ctx.guild.voice_client
        volume = player.volume
        duration_in_seconds = track.length / 1000  # Convert milliseconds to seconds
        current_time = player.position / 1000  # Convert milliseconds to seconds
        time = await self.format_time(duration_in_seconds)
        embed = Embed(title="<a:onfire:1170817312975224893> Now playing", description=f"```{track.title}```", color=discord.Color.blue())
        embed.set_image(url=track.thumb)
        embed.add_field(name="<a:spin:1170816054499491872> Duration", value=f"``{time}``", inline=True)
        embed.add_field(name="<a:movingspeaker:1170818120630403092> Volume", value=f"```{volume}/100```", inline=True)
        embed.set_footer(text=f"{len(player.queue)} songs in queue.")
        return embed
    except Exception as e:
        print(f"An error occurred: {e}")
        await ctx.send("An error occurred while searching for tracks.")
  
  @commands.guild_only()
  @commands.hybrid_command(name="play", description="Add music to queue with `/play <url>`")
  async def _play(self, ctx, *, query):
      channel = ctx.author.voice.channel
      tracks: list[wavelink.YouTubeTrack] = await wavelink.YouTubeTrack.search(query)
      player: wavelink.Player = ctx.guild.voice_client
      if not player:
          player: wavelink.Player = await channel.connect(cls=wavelink.Player)
          player.autoplay = True
          if "&list" in query or "?list" in query:
              playlist = await wavelink.YouTubePlaylist.convert(ctx, query)
              if "index=" in query:
                  index = (int(query.split("&index=")[1]) - 1) if "&index=" in query else 0
                  track = playlist.tracks[index]
              else:
                  track = playlist.tracks[0]
              embed = Embed(title="⚠️ Warning!", description=f"Do you want to add \n`{track.title}`\n\n**Or**\n\n`{len(playlist.tracks)}` songs to the queue?")
              embed.set_thumbnail(url=track.thumb)
              await ctx.send(embed=embed, view=PlaylistView(ctx, player, playlist, track))
          else:
              await player.play(tracks[0])
              await asyncio.sleep(1)
              curr_track = player.current
              embed = await self.create_now_playing_embed(ctx, curr_track)
              message = await ctx.send(embed=embed, view=PlayingView(ctx, player))
      else:
          if "&list" in query or "?list" in query:
              playlist = await wavelink.YouTubePlaylist.convert(ctx, query)
              if "index=" in query:
                  index = (int(query.split("&index=")[1]) - 1) if "&index=" in query else 0
                  track = playlist.tracks[index]
              else:
                  track = playlist.tracks[0]
              embed = Embed(title="⚠️ Warning!", description=f"Do you want to add \n\n`{track.title}`\n\n**Or**\n\n`{len(playlist.tracks)}` songs to the queue?",color=discord.Color.blue())
              embed.set_footer(text=f"{len(player.queue)} songs in the queue.")
              embed.set_thumbnail(url=track.thumb)
              await ctx.send(embed=embed, view=PlaylistPlayingView(ctx, player, playlist, track))
          else:
              if player.is_playing() and not player.paused:
                  # The player is currently playing and not paused, so we can queue the track.
                  player.queue(tracks[0])
                  embed = Embed(title="➕ Added to queue", description=f"`{tracks[0].title}`", color=discord.Color.blue())
                  embed.set_footer(text=f"{len(player.queue)} songs in the queue.")
                  embed.set_thumbnail(url=tracks[0].thumb)
                  await ctx.send(embed=embed)
              elif not player.is_playing() and not player.paused and len(player.queue) == 0:
                  # If the player is not playing, not paused, and the queue is empty, start playing the track.
                  await player.play(tracks[0])
                  curr_track = player.current
                  embed = await self.create_now_playing_embed(ctx, curr_track)
                  message = await ctx.send(embed=embed, view=PlayingView(ctx, player))
              else:
                  player.queue(tracks[0])
                  embed = Embed(title="➕ Added to queue", description=f"`{tracks[0].title}`", color=discord.Color.blue())
                  embed.set_footer(text=f"{len(player.queue)} songs in the queue.")
                  embed.set_thumbnail(url=tracks[0].thumb)
                  await ctx.send(embed=embed)
            
  @commands.command(name="lofi", description="Play lofi radio.")  # Use @commands.command instead of @commands.hybrid_command
  @commands.guild_only()
  async def _lofi(self, ctx):
      search = "https://www.youtube.com/watch?v=IRp0zhUFi-M"
      if not ctx.guild.voice_client:
        vc: wavelink.Player = await ctx.author.voice.channel.connect(cls=wavelink.Player)
      else:
        vc: wavelink.Player = ctx.guild.voice_client
      tracks: list[wavelink.YouTubeTrack] = await wavelink.YouTubeTrack.search(search)
      if not tracks:
        await ctx.send(f'Sorry I could not find any songs with search: `{search}`')
        return
      track: wavelink.YouTubeTrack = tracks[0]
      embed = Embed(title="<a:onfire:1170817312975224893> Now playing", description=f"```LOFI RADIO```", color=discord.Color.blue())
      embed.add_field(name="<a:spin:1170816054499491872> Duration", value=f"```STREAM```", inline=True)
      embed.add_field(name="<a:movingspeaker:1170818120630403092> Volume", value=f"```{vc.volume}/100```", inline=True)
      embed.set_footer(text=f"{len(vc.queue)} songs in queue.")
      await ctx.send(embed=embed)
      await vc.play(track)

  @commands.guild_only()
  @commands.hybrid_command(name="nowplaying", description="Show current player with current song playing.")
  async def _nowplaying(self, ctx):
      player: wavelink.Player = ctx.guild.voice_client
      if player and player.is_playing:
          # Send the initial message
          curr_track = player.current
          embed = await self.create_now_playing_embed(ctx, curr_track)
          message = await ctx.send(embed=embed, view=PlayingView(ctx, player))
      else:
          await ctx.send('Nothing is currently playing.')

  @commands.guild_only()
  @commands.command(name="queue", description="View the top songs in the queue.")
  async def _queue(self, ctx):
      player: wavelink.Player = ctx.guild.voice_client
      if not player or not player.is_connected:
          await ctx.send("I am not connected to a voice channel.")
          return
      if not player.queue:
          await ctx.send("The queue is empty.")
          return
      # Get the first 10 items in the queue and number them
      queue_items = []
      for i, item in enumerate(player.queue):
          if i >= 10:
              break
          queue_items.append(f"```{i + 1}. {str(item)}```")
      # Join the numbered items with "\n" separator
      queue_str = "\n".join(queue_items)
      embed = Embed(title="🎵 Queue (First 10 Songs)")
      embed.add_field(name="Queue:", value=queue_str, inline=False)
      embed.set_footer(text=f"{len(player.queue)} songs in queue.")
      await ctx.send(embed=embed)
  
  @commands.guild_only()
  @commands.hybrid_command(name="skip", description="Skip a song.")
  async def _skip(self, ctx):
      player: wavelink.Player = ctx.guild.voice_client
      if player and player.is_playing():
          await player.stop(force=True)
          await ctx.send("```Skipped the current song.```")
      else:
          await ctx.send("```⛔ Nothing is currently playing.```")
        
  @commands.guild_only()
  @commands.hybrid_command(name="previous", description="View previous song.")
  async def _previous(self, ctx):
      player: wavelink.Player = ctx.guild.voice_client
      if player and len(player.queue.history) > 0:
          prev_track = player.queue.history[-2]  # Get the last song in the history
          await player.play(prev_track)
          await ctx.send(f"```Playing {prev_track.title}```")
      else:
          await ctx.send("```⛔ No previous track to play.```")
        
  @commands.guild_only()
  @commands.hybrid_command(name="clear", description="Clear all the songs from queue.")
  async def _clearqueue(self, ctx):
    player: wavelink.Player = ctx.guild.voice_client
    if player:
        player.queue.reset()
        await ctx.send("```Queue cleared.```")
    else:
        await ctx.send("```⛔ No queue to clear.```")
      
  @commands.guild_only()
  @commands.hybrid_command(name="shuffle", description="Shuffle all the songs in the queue.")
  async def _shuffle(self, ctx):
      player: wavelink.Player = ctx.guild.voice_client
      if player:
        player.queue.shuffle()
        await ctx.send("```Queue Shuffled.```")
      else:
        return await ctx.send("```⛔ The bot is disconnected.```")
        
  @commands.guild_only()
  @commands.hybrid_command(name="pause", description="Pause the current playing song.")
  async def _pause(self, ctx):
      player: wavelink.Player = ctx.guild.voice_client
      if player:
        await player.pause()
        await ctx.send("Paused")
      else:
        return await ctx.send("```⛔ The bot is disconnected.```")
        
  @commands.guild_only()
  @commands.hybrid_command(name="resume", description="Resume the current playing song.")
  async def _resume(self, ctx):
      player: wavelink.Player = ctx.guild.voice_client
      if player:
        await player.resume()
        await ctx.send("Resumed.")
      else:
        return await ctx.send("```⛔ The bot is disconnected.```")
        
  @commands.guild_only()
  @commands.hybrid_command(name="stop", description="Disconnect bot from the voice channel.")
  async def _disconnect(self, ctx):
      player: wavelink.Player = ctx.guild.voice_client
      if player:
        await player.disconnect()
        await ctx.send("```⛔ Disconnected```")
      else:
        return await ctx.send("```⛔ The bot is not connected.```")
        
  @commands.guild_only()
  @commands.hybrid_command(name="volume", description="Set the volume for the bot from 0% to 100%.")
  async def _vol(self, ctx, volume: int):
      player: wavelink.Player = ctx.guild.voice_client
      if volume > 100:
          return await ctx.send("```⛔ 100% Is Max```")
      elif volume < 0:
          return await ctx.send("```⛔ 0% Is Lowest```")
      await player.set_volume(volume)
      await ctx.send(f"```Volume set to %{volume}```")

  @commands.guild_only()
  @commands.hybrid_command(name="repeatall", description="Repeat the queue.")
  async def _loopall(self, ctx):
      player: wavelink.Player = ctx.guild.voice_client
      if player:
        if player.queue.loop_all == True:
            player.queue.loop_all = False
            await ctx.send("```Repeat all off.```")
        else:
            player.queue.loop_all = True
            await ctx.send("```Repeat all on.```")
      else:
        await ctx.send(f"```⛔ No player connected.```")

  @commands.guild_only()
  @commands.hybrid_command(name="repeat", description="Repeat the current song.")
  async def _loop(self, ctx):
      player: wavelink.Player = ctx.guild.voice_client
      if player:
        if player.queue.loop == True:
            player.queue.loop = False
            await ctx.send("Repeat off.")
        else:
            player.queue.loop = True
            await ctx.send("```Repeat on.```")
      else:
        await ctx.send(f"```⛔ No player connected.```") 

  @commands.hybrid_command(name='about', description="Information about the bot.")
  @commands.cooldown(1, 15, commands.BucketType.user)
  async def _about(self, ctx):
      guild_count = len(self.bot.guilds)
      invite_link = discord.utils.oauth_url(self.bot.user.id, permissions=discord.Permissions(permissions=964525804865))
      server_link = "https://discord.gg/atlasdev"
      embed=Embed(description="[Invite Me](" + invite_link + ") to your server!\n[Support](" + server_link + ")\n\n I'm a bot built with python by **cfunkz#6969**.", color=discord.Color.green())
      embed.add_field(name='420 GUILDS', value=guild_count)
      await ctx.send(embed=embed, view=InviteButton(str(invite_link)))

  @commands.hybrid_command(name='help', description="Brings out the help panel or view command description with `/help <command name>`")
  @commands.cooldown(1, 1, commands.BucketType.user)
  async def _help(self, ctx, *, command_or_item=None):
      if command_or_item:
          # Check if the query matches a command
          command = self.bot.get_command(command_or_item)
          if command:
              embed = Embed(title=f"Command: {command.name}", description=command.description)
              embed.set_footer(text="Type /help to get the general help panel")
              await ctx.send(embed=embed)
              return
          await ctx.send(f"No command named '{command_or_item}' found.")
          return

      # Display general help panel
      embed = Embed(title="📚 Help Command", description="Here are some available commands:")
      for cog in self.bot.cogs.values():
          commands_list = [f"**{command.name}** - {command.description}" for command in cog.get_commands()]
          if commands_list:
              embed.add_field(name=f"**{cog.qualified_name}**", value="\n".join(commands_list), inline=False)
      embed.set_footer(text="Type /help <command name> to get the description of a specific command")
      message = await ctx.send(embed=embed, ephemeral=True)

  @commands.hybrid_command(name="ping", description="Pings the bot for its latency.")
  async def _ping(self, ctx):
    # Measure the time before the API call
    start_time = time.time()
    # Make an API call. In this case, fetch a channel's information.
    await self.bot.fetch_channel(ctx.channel.id)
    # Measure the time after the API call
    end_time = time.time()
    # The difference (in milliseconds) is a rough estimate of the API response time.
    api_latency = round((end_time - start_time) * 1000)
    # bot.latency is in seconds, so convert to milliseconds
    ws_latency = round(self.bot.latency * 1000)
    embed = Embed(title="Latency")
    embed.add_field(name="Ping", value=f"```{api_latency}ms```")
    embed.add_field(name="Websocket", value=f"```{ws_latency}ms```")
    await ctx.send(embed=embed)

async def setup(bot):
    cog = MusicCommands(bot)
    await bot.add_cog(cog)
