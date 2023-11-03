import discord
from discord.ext import commands
from discord import app_commands
import wavelink
from config import dtoken, ip_add, password

intents = discord.Intents.all()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix=commands.when_mentioned_or('420 '), intents=intents, activity = discord.Game(name="/help"))

    async def on_ready(self):
        print(f'Logged in {self.user} | {self.user.id}')
        node: wavelink.Node = wavelink.Node(uri=ip_add, password=password)
        await wavelink.NodePool.connect(client=self, nodes=[node])
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

bot = Bot()
bot.run(dtoken)
