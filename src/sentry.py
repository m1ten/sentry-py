import discord
from discord.ext import commands

# load env from .env
try:
    import dotenv
    import os

    dotenv.load_dotenv()

    TOKEN = os.getenv('TOKEN')
    APP_ID = os.getenv('APP_ID')
    GUILD_ID = os.getenv('GUILD_ID')
    PREFIX = os.getenv('PREFIX')  # deprecated
except Exception as e:
    print(f'Error: {e}')
    exit(1)


def logging() -> None:
    import logging

    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(
        filename='sentry.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter(
        '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)


class Bot(commands.Bot):

    def __init__(self) -> None:
        super().__init__(
            command_prefix=PREFIX, # deprecated
            intents=discord.Intents.all(),
            application_id=APP_ID
        )

    async def setup_hook(self) -> None:
        # for ext in self.initial_extensions:
        #     await self.load_extension(ext)

        await self.load_extension('src.cogs.setup')

        await bot.tree.sync(guild=discord.Object(id=GUILD_ID))

    async def close(self) -> None:
        await super().close()
    
    async def on_ready(self) -> None:
        print(f'Logged on as {self.user}!')

        # set the custom status to 'you are not the owner of me'
        await self.change_presence(
            activity=discord.Activity(
                name='you are not the owner of me',
                type=discord.ActivityType.playing
            )
        )


bot = Bot()


def main() -> None:
    bot.run(TOKEN)
