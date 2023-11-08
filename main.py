import discord
from discord.ext import commands
import wavelink
from wavelink.ext import spotify
from config import dtoken, freeURL, freePASS, spotifyUSER, spotifySECRET, ip_add, secret
import logging
import asyncio

intents = discord.Intents.all()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=intents, activity = discord.Game(name="/help OR !help"), help_command=None)


    async def on_wavelink_track_start(self, node, payload):
        print(f"Track started: {payload.track.title}")
    
    async def on_wavelink_player_update(self, node, payload):
        print(f"Player update - Volume: {payload.volume}, Position: {payload.position}")
    
    # Handle errors
    async def on_wavelink_node_error(self, node, error):
        print(f"Node error: {error}")
    
    async def on_wavelink_track_error(self, node, payload, error):
        print(f"Track error: {error}")

    async def on_wavelink_node_ready(self, node: wavelink.Node):
        print(f"Node {node.id} is ready!")

    async def on_ready(self):
        print(f'Logged in {self.user} | {self.user.id}')
        sc = spotify.SpotifyClient(
            client_id=spotifyUSER,
            client_secret=spotifySECRET
        )
        node: wavelink.Node = wavelink.Node(uri=freeURL, secure=True, password=freePASS)
        await wavelink.NodePool.connect(client=self, nodes=[node], spotify=sc)
        print("Lavalink Connected!")
        await self.load_cogs()  # Call your load_cogs function here
        #synced = await self.tree.sync()
        #print(f"{len(synced)}")

    async def load_cogs(self): #Load the cogs
      cogs = ['commands']
      for cog in cogs:
          try:
              await self.load_extension(f'cogs.{cog}')
              print(f'Loaded cog: {cog}')
          except Exception as e:
              print(f'Failed to load cog: {cog}\n\nError: {str(e)}')
              
discord.utils.setup_logging(level=logging.INFO, root=False)

bot = Bot()

if __name__ == "__main__":
    asyncio.run(bot.start(dtoken))
