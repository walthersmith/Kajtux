import io
import random

import googletrans
import requests
from discord.ext import commands
from discord.ext import menus
import discord
import re

from extensions.utils.paginator import RoboPages


class Fun(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='urban')
    async def _urban(self, ctx, *, word):
        """Searches urban dictionary."""

        url = f'http://api.urbandictionary.com/v0/define?term={word}'
        resp = requests.get(url)
        if resp.status_code != 200:
            return await ctx.send(f'An error occurred: {resp.status_code} {resp.reason}')

        js =  resp.json()
        data = js.get('list', [])
        if not data:
            return await ctx.send('No results found, sorry.')

        pages = RoboPages(UrbanDictionaryPageSource(data))
        try:
            await pages.start(ctx)
        except menus.MenuError as e:
            await ctx.send(e)


    @commands.command(name="cat")
    async def cat(self, ctx):
        """Gives you a random cat."""
        url = 'https://api.thecatapi.com/v1/images/search'
        resp = requests.get(url)
        if resp.status_code != 200:
            return await ctx.send('No cat found :(')
        js = resp.json()
        await ctx.send(embed=discord.Embed(title='Random Cat').set_image(url=js[0]['url']))

    @commands.command(name="dog")
    async def dog(self, ctx):
        """Gives you a random dog."""
        url = 'https://random.dog/woof'
        resp = requests.get(url)
        if resp.status_code != 200:
            return await ctx.send('No dog found :(')

        filename = resp.text
        url = f'https://random.dog/{filename}'
        filesize = ctx.guild.filesize_limit if ctx.guild else 8388608

        if filename.endswith(('.mp4', '.webm')):
            async with ctx.typing():
                other = requests.get(url)
                if other.status_code != 200:
                    return await ctx.send('Could not download dog video :(')

                if int(other.headers['Content-Length']) >= filesize:
                    return await ctx.send(f'Video was too big to upload... See it here: {url} instead.')

                fp = io.BytesIO(other.content)
                await ctx.send(file=discord.File(fp, filename=filename))
        else:
            await ctx.send(embed=discord.Embed(title='Random Dog').set_image(url=url))

    @commands.command(hidden=True)
    async def translate(self, ctx, *, message: commands.clean_content = None):
        """Translates a message to English using Google translate."""

        loop = self.bot.loop
        if message is None:
            ref = ctx.message.reference
            if ref and isinstance(ref.resolved, discord.Message):
                message = ref.resolved.content
            else:
                return await ctx.send('Missing a message to translate')

        try:
            ret = await loop.run_in_executor(None, self.trans.translate, message)
        except Exception as e:
            return await ctx.send(f'An error occurred: {e.__class__.__name__}: {e}')

        embed = discord.Embed(title='Translated', colour=0x4284F3)
        src = googletrans.LANGUAGES.get(ret.src, '(auto-detected)').title()
        dest = googletrans.LANGUAGES.get(ret.dest, 'Unknown').title()
        embed.add_field(name=f'From {src}', value=ret.origin, inline=False)
        embed.add_field(name=f'To {dest}', value=ret.text, inline=False)
        await ctx.send(embed=embed)


    @commands.command()
    async def love(self, ctx):
        """What is love?"""
        responses = [
            'https://www.youtube.com/watch?v=HEXWRTEbj1I',
            'https://www.youtube.com/watch?v=i0p1bmr0EmE',
            'an intense feeling of deep affection',
            'something we don\'t have'
        ]

        response = random.choice(responses)
        await ctx.send(response)


    @commands.command(hidden=True)
    async def bored(self, ctx):
        """boredom looms"""
        await ctx.send('http://i.imgur.com/BuTKSzf.png')

class UrbanDictionaryPageSource(menus.ListPageSource):
    BRACKETED = re.compile(r'(\[(.+?)\])')
    def __init__(self, data):
        super().__init__(entries=data, per_page=1)

    def cleanup_definition(self, definition, *, regex=BRACKETED):
        def repl(m):
            word = m.group(2)
            return f'[{word}](http://{word.replace(" ", "-")}.urbanup.com)'

        ret = regex.sub(repl, definition)
        if len(ret) >= 2048:
            return ret[0:2000] + ' [...]'
        return ret

    async def format_page(self, menu, entry):
        maximum = self.get_max_pages()
        title = f'{entry["word"]}: {menu.current_page + 1} out of {maximum}' if maximum else entry['word']
        embed = discord.Embed(title=title, colour=0xE86222, url=entry['permalink'])
        embed.set_footer(text=f'by {entry["author"]}')
        embed.description = self.cleanup_definition(entry['definition'])

        try:
            up, down = entry['thumbs_up'], entry['thumbs_down']
        except KeyError:
            pass
        else:
            embed.add_field(name='Votes', value=f'\N{THUMBS UP SIGN} {up} \N{THUMBS DOWN SIGN} {down}', inline=False)

        try:
            date = discord.utils.parse_time(entry['written_on'][0:-1])
        except (ValueError, KeyError):
            pass
        else:
            embed.timestamp = date

        return embed

def teardown(bot):
    print('Fun: I am being unloaded!')

def setup(bot):
    bot.add_cog(Fun(bot))
    print('Fun: loaded!')