import discord
from discord.ext import commands
from discord.ui import button, View
from discord import Embed
import wavelink
import asyncio

class PlaylistView(View):
    def __init__(self, ctx, player, playlist, track):
        super().__init__(timeout=120)
        self.player = player
        self.user_id = ctx.author.id
        self.track = track
        self.ctx = ctx
        self.playlist = playlist
      
    async def on_timeout(self):
        self.stop()

    @button(label="ADD SONG", style=discord.ButtonStyle.grey, emoji="🎵")
    async def add_one(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("Only command caller can do that.", ephemeral=True)
        await self.player.play(self.track)
        embed = Embed(title="🎶 Now playing", description=f"`{self.track.title}`", color=discord.Color.blue())
        embed.set_footer(text=f"{len(self.player.queue)} songs in the queue.")
        embed.set_image(url=self.track.thumb)
        await interaction.response.send_message(embed=embed, view=PlayingView(self.ctx, self.player))
        self.stop()
  
    @button(label="ADD ALL", style=discord.ButtonStyle.grey, emoji="🎶")
    async def add_all_queue(self, interaction: discord.Interaction, button: discord.ui.Button):
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("Only command caller can do that.", ephemeral=True)
        self.player.queue(self.playlist)
        await self.player.play(self.playlist.tracks[0])
        embed = Embed(title=f"{len(self.playlist.tracks)} Songs", description=f"Added to queue from `{self.playlist.name.title()}` playlist.", color=discord.Color.blue())
        embed.set_footer(text=f"{len(self.player.queue)} songs in the queue.")
        embed.set_image(url=self.playlist.tracks[0].thumb)
        await interaction.response.send_message(embed=embed)
        self.stop()

class PlaylistPlayingView(View):
  def __init__(self, ctx, player, playlist, track):
      super().__init__(timeout=120)
      self.player = player
      self.track = track
      self.user_id = ctx.author.id
      self.playlist = playlist

  async def on_timeout(self):
      self.stop()
      await self.message.delete()

  @button(label="ADD SONG", style=discord.ButtonStyle.grey, emoji="🎵")
  async def add_one2(self, interaction: discord.Interaction, button: discord.ui.Button):
      if interaction.user.id != self.user_id:
          return await interaction.response.send_message("Only command caller can do that.", ephemeral=True)
      if self.player.is_paused():
          self.player.queue(self.track)
      else:
          await self.player.play(self.track)
      embed = Embed(title=f"➕ Added to queue", description=f"`{self.track.title}`", color=discord.Color.blue())
      embed.set_image(url=self.track.thumb)
      embed.set_footer(text=f"{len(self.player.queue)} songs in the queue.")
      await interaction.response.send_message(embed=embed)
      self.stop()

  @button(label="ADD ALL", style=discord.ButtonStyle.grey, emoji="🎶")
  async def add_all_queue2(self, interaction: discord.Interaction, button: discord.ui.Button):
      if interaction.user.id != self.user_id:
          return await interaction.response.send_message("Only command caller can do that.", ephemeral=True)
      if self.player.is_paused():
          self.player.queue(self.playlist)
      else:
          self.player.queue(self.playlist)
          await self.player.play(self.playlist.tracks[0])
      self.player.queue(self.playlist)
      embed = Embed(title=f"{len(self.playlist.tracks)} Songs", description=f"Added to queue from `{self.playlist.name.title()}` playlist.", color=discord.Color.blue())
      embed.set_footer(text=f"{len(self.player.queue)} songs in the queue.")
      embed.set_image(url=self.playlist.tracks[0].thumb)
      await interaction.response.send_message(embed=embed)
      self.stop()


class PlayingView(View):
    def __init__(self, ctx, player):
        super().__init__(timeout=None)
        self.player = player
        self.user_id = ctx.author.id
        self.ctx = ctx
      
    async def on_timeout(self):
        self.stop()

    @button(style=discord.ButtonStyle.grey, emoji="⏮️", row=0)
    async def _previoustrack(self, interaction: discord.Interaction, button: discord.ui.Button):
      if interaction.user.id != self.user_id:
        return await interaction.response.send_message("Only command caller can do that.", ephemeral=True)
      try:
        if self.player and len(self.player.queue.history) > 0:
            prev_track = self.player.queue.history[-2]  # Get the last song in the history
            curr_track = self.player.current
            self.player.queue.put_at_front(curr_track)
            await self.player.play(prev_track)
            await asyncio.sleep(1)
            await interaction.response.send_message(f"```⏮️ Playing **{prev_track.title}**```", ephemeral=True)
      except:
        return await interaction.response.send_message("```⛔ Error! No previous track or not connected.```", ephemeral=True)
  
    @button(style=discord.ButtonStyle.grey, emoji="⏯️", row=0)
    async def play_pause(self, interaction: discord.Interaction, button: discord.ui.Button):
        player: wavelink.Player = self.ctx.guild.voice_client
        if interaction.user.id != self.user_id:
            return await interaction.response.send_message("Only command caller can do that.", ephemeral=True)
        if not player.is_playing() and player.current:
            await player.resume()
            await interaction.response.send_message("```▶️ Resumed.```", ephemeral=True)
        elif player.is_playing():
            await player.pause()
            await interaction.response.send_message("```⏸️ Paused.```", ephemeral=True)
        else:
            return await interaction.response.send_message("```⛔ Error! No track or not connected.```", ephemeral=True)

    @button(style=discord.ButtonStyle.grey, emoji="⏭️", row=0)
    async def _nexttrack(self, interaction: discord.Interaction, button: discord.ui.Button):
      if interaction.user.id != self.user_id:
        return await interaction.response.send_message("Only command caller can do that.", ephemeral=True)
      if self.player and len(self.player.queue) > 0:
          next_track = self.player.queue[0]
          await self.player.stop(force=True)
          await interaction.response.send_message(f"```⏭️ Playing **{next_track.title}**```", ephemeral=True)
          await asyncio.sleep(1)
      else:
          return await interaction.response.send_message("```⛔ Error! No next track or not connected.```", ephemeral=True)
  
    @button(style=discord.ButtonStyle.grey, emoji="🔀", row=0)
    async def _shuffle(self, interaction: discord.Interaction, button: discord.ui.Button):
      if interaction.user.id != self.user_id:
        return await interaction.response.send_message("Only command caller can do that.", ephemeral=True)
      if self.player:
          self.player.queue.shuffle()
          await interaction.response.send_message("```🔀 Queue Shuffled.```")
      else:
          return await interaction.response.send_message("```⛔ Error! Not connected```", ephemeral=True)

    @button(style=discord.ButtonStyle.grey, emoji="🔁", row=0)
    async def _repeat(self, interaction: discord.Interaction, button: discord.ui.Button):
      if interaction.user.id != self.user_id:
        return await interaction.response.send_message("Only command caller can do that.", ephemeral=True)
      if self.player:
          if self.player.queue.loop:
              self.player.queue.loop = False
              await interaction.response.send_message("```🔁 Repeat off.```", ephemeral=True)
          else:
              self.player.queue.loop = True
              await interaction.response.send_message("```🔁 Repeat on.```", ephemeral=True)
      else:
          return await interaction.response.send_message("```⛔ Error! Not connected```", ephemeral=True)

    @button(style=discord.ButtonStyle.grey, emoji="🔈", row=1)
    async def _volumedown(self, interaction: discord.Interaction, button: discord.ui.Button):
      if interaction.user.id != self.user_id:
        return await interaction.response.send_message("Only command caller can do that.", ephemeral=True)
      volume = self.player.volume
      new_volume = (volume - 10)
      if new_volume < 0:
          return await interaction.response.send_message("```0% Is Lowest```")
      else:
          await interaction.response.send_message(f"```🔈 Decreased to {new_volume}%```", ephemeral=True)
          await self.player.set_volume(new_volume)

    @button(style=discord.ButtonStyle.grey, emoji="🔊", row=1)
    async def _volumeup(self, interaction: discord.Interaction, button: discord.ui.Button):
      if interaction.user.id != self.user_id:
        return await interaction.response.send_message("Only command caller can do that.", ephemeral=True)
      volume = self.player.volume
      new_volume = (volume + 10)
      if new_volume > 100:
          return await interaction.response.send_message("```100% Is Highest.```")
      else:
          await interaction.response.send_message(f"```🔊 Increased to {new_volume}%```", ephemeral=True)
          await self.player.set_volume(new_volume)

    @button(style=discord.ButtonStyle.grey, emoji="🧹", row=1)
    async def _clearqueue(self, interaction: discord.Interaction, button: discord.ui.Button):
      if interaction.user.id != self.user_id:
        return await interaction.response.send_message("```Only command caller can do that.```", ephemeral=True)
      self.player.queue.reset()
      await interaction.response.send_message("```Queue cleared!```", ephemeral=True)

    @button(style=discord.ButtonStyle.grey, emoji="🚫", row=1)
    async def _dc(self, interaction: discord.Interaction, button: discord.ui.Button):
      if interaction.user.id != self.user_id:
        return await interaction.response.send_message("```Only command caller can do that.```", ephemeral=True)
      await self.player.disconnect()
      await interaction.response.send_message("```🚫 Disconnected```", ephemeral=True)

class InviteButton(View):
  def __init__(self, inv: str):
      super().__init__()
      self.inv = inv
      self.add_item(discord.ui.Button(label = "Invite", url = self.inv))

  @button(label="Support", style=discord.ButtonStyle.blurple)
  async def supportButton(self, interaction: discord.Interaction, button: discord.ui.Button):
      url = "https://discord.gg/atlasdev"
      await interaction.response.send_message(url, ephemeral=True)


class QueueView(View):
  def __init__(self, ctx, player):
      super().__init__(timeout=None)
      self.ctx = ctx
      self.player = player
      self.page = 0

  async def show_queue_page(self):
    queue = self.player.queue
    total_pages = len(queue)

  @button(style=discord.ButtonStyle.grey, emoji="⬅️")
  async def prev_page(self):
      if self.page > 0:
          self.page -= 1
          await self.show_queue_page()

  @button(style=discord.ButtonStyle.grey, emoji="➡️")
  async def next_page(self):
      total_pages = (len(self.player.queue) - 1) // 10 + 1
      if self.page < total_pages - 1:
          self.page += 1
          await self.show_queue_page()
