import discord
from discord.ext import commands
import wavelink
from wavelink.ext import spotify
from config import dtoken, freeURL, freePASS, spotifyUSER, spotifySECRET, ip_add, secret
import logging

intents = discord.Intents.all()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('!'), intents=intents, activity = discord.Game(name="/help OR !help"), help_command=None)

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
              
discord.utils.setup_logging(level=logging.DEBUG, root=False)

bot = Bot()

@bot.event
async def on_wavelink_node_ready(node: Node) -> None:
    print(f"Node {node.id} is ready!")

bot.run(dtoken)
