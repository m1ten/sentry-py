import discord
from discord import app_commands
from discord.ext import commands

import requests
import json


class wiki(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name='wiki', description='get a wiki page')
    async def wiki(self, interaction: discord.Interaction, name: str, ephemeral: bool) -> None:

        # check if command is being ran in NSFW channel
        if not interaction.channel.is_nsfw():
            await interaction.response.send_message(f'This command can only be used in NSFW channels.', ephemeral=True)
            return

        # replace spaces with underscores
        name = name.replace(' ', '_')

        # get the wiki page
        wiki_page = requests.get(
            f'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&exintro=&explaintext=&titles={name}')

        # get json data
        wiki_data = json.loads(wiki_page.text)
        wiki_data = wiki_data['query']['pages'].popitem()[1]

        TITLE = wiki_data['title']
        SUMMARY = wiki_data['extract'] if 'extract' in wiki_data else None

        if not SUMMARY:
            # await interaction.response.send_message(f'`{name}` not found, please try narrowing the search.', ephemeral=True)

            # search query with the name
            search_query = requests.get(
                f'https://en.wikipedia.org/w/api.php?action=query&list=search&format=json&srsearch={name}')

            # get json data
            search_data = json.loads(search_query.text)

            # separate the result by name and append it to the list
            search_data = search_data['query']['search']
            search_data = [x['title'] for x in search_data]

            # if there is no result, return
            if not search_data:
                await interaction.response.send_message(f'`{name}` not found, please try narrowing the search.', ephemeral=True)
                return

            # keep 5 results, digard the rest
            search_data = search_data[:5]

            # Send the list of results in a discord dropdown menu

            class Select(discord.ui.Select):
                def __init__(self):
                    options = []

                    for x in search_data:
                        options.append(discord.SelectOption(
                            label=x, description=x))

                    super().__init__(placeholder='Select an option.',
                                     max_values=1, min_values=1, options=options)

                async def callback(self, interaction: discord.Interaction):

                    # get name from the selected option
                    name = self.values[0].replace(' ', '_')

                    # get the wiki page
                    wiki_page = requests.get(
                        f'https://en.wikipedia.org/w/api.php?action=query&prop=extracts&format=json&exintro=&explaintext=&titles={name}')

                    # get json data
                    wiki_data = json.loads(wiki_page.text)
                    wiki_data = wiki_data['query']['pages'].popitem()[1]

                    TITLE = wiki_data['title']
                    SUMMARY = wiki_data['extract']

                    # get image from wiki page
                    try:
                        wiki_image = requests.get(
                            f'https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&titles={name}')
                        wiki_image_data = json.loads(wiki_image.text)
                        image = wiki_image_data['query']['pages'].popitem()[
                            1]['thumbnail']['source']

                        if '50px' in image:
                            IMAGE = image.replace('50px', '175px')
                    except KeyError:
                        IMAGE = None

                    # embed wiki page
                    embed = discord.Embed(title=TITLE, description=SUMMARY[:750] + '...', color=0x000000,
                                          url=f'https://en.wikipedia.org/wiki/{name}')

                    try:
                        embed.set_image(url=IMAGE)
                    except UnboundLocalError:
                        pass

                    embed.set_footer(text='Powered by Wikipedia',
                                     icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/1122px-Wikipedia-logo-v2.svg.png')

                    await interaction.response.send_message(embed=embed, ephemeral=ephemeral)

            class SelectView(discord.ui.View):
                def __init__(self, *, timeout=180):
                    super().__init__(timeout=timeout)
                    self.add_item(Select())

            await interaction.response.send_message(f'Multiple results found for `{name}`.', view=SelectView(), ephemeral=True)

            return

        # get image from wiki page
        try:
            wiki_image = requests.get(
                f'https://en.wikipedia.org/w/api.php?action=query&prop=pageimages&format=json&titles={name}')
            wiki_image_data = json.loads(wiki_image.text)
            image = wiki_image_data['query']['pages'].popitem()[
                1]['thumbnail']['source']

            if '50px' in image:
                IMAGE = image.replace('50px', '175px')
        except KeyError:
            IMAGE = None

        # embed wiki page
        embed = discord.Embed(title=TITLE, description=SUMMARY[:750] + '...', color=0x000000,
                              url=f'https://en.wikipedia.org/wiki/{name}')

        try:
            embed.set_image(url=IMAGE)
        except UnboundLocalError:
            pass

        embed.set_footer(text='Powered by Wikipedia',
                         icon_url='https://upload.wikimedia.org/wikipedia/commons/thumb/8/80/Wikipedia-logo-v2.svg/1122px-Wikipedia-logo-v2.svg.png')

        await interaction.response.send_message(embed=embed, ephemeral=ephemeral)
