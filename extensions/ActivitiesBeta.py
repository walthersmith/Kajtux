import discord
from discord.ext import commands
from discord.utils import get
from discordTogether import DiscordTogether


class ActivitiesBeta(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.debug = True
        self.togetherControl = DiscordTogether(bot)

    @commands.command(name="yt", aliases=["youtube"])
    async def ytt(self, ctx):
        voice_state = ctx.message.author.voice
        if voice_state is not None:
            link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 'youtube')
            emoji = get(ctx.guild.emojis, name="party")
            embed = discord.Embed(
                title="Click en el link para iniciar (BETA)",
                description=f'[{emoji} Iniciar en el canal: {ctx.author.voice.channel.name} {emoji}]({link})',
                color=discord.Colour.red(),
            )
            await ctx.send(embed=embed)

        else:
            await ctx.send('**Para usar este comando necesitas unirte a un canal de voz**')

    @commands.command(name="poker")
    async def poker(self, ctx):
        voice_state = ctx.message.author.voice
        if voice_state is not None:
            link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 'poker')
            emoji = get(ctx.guild.emojis, name="party")
            embed = discord.Embed(
                title="Click en el link para iniciar (BETA)",
                description=f'[{emoji} Iniciar en el canal: {ctx.author.voice.channel.name} {emoji}]({link})',
                color=discord.Colour.red(),
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send('**Para usar este comando necesitas unirte a un canal de voz**')

    @commands.command(name="betrayal")
    async def betrayal(self, ctx):
        voice_state = ctx.message.author.voice
        if voice_state is not None:
            link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 'betrayal')
            emoji = get(ctx.guild.emojis, name="party")
            embed = discord.Embed(
                title="Click en el link para iniciar (BETA)",
                description=f'[{emoji} Iniciar en el canal: {ctx.author.voice.channel.name} {emoji}]({link})',
                color=discord.Colour.red(),
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send('**Para usar este comando necesitas unirte a un canal de voz**')

    @commands.command(name="fishing")
    async def fishing(self, ctx):
        voice_state = ctx.message.author.voice
        if voice_state is not None:
            link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 'fishing')
            emoji = get(ctx.guild.emojis, name="party")
            embed = discord.Embed(
                title="Click en el link para iniciar (BETA)",
                description=f'[{emoji} Iniciar en el canal: {ctx.author.voice.channel.name} {emoji}]({link})',
                color=discord.Colour.red(),
            )
            await ctx.send(embed=embed)

        else:
            await ctx.send('**Para usar este comando necesitas unirte a un canal de voz**')

    @commands.command(name="chess")
    async def chess(self, ctx):
        voice_state = ctx.message.author.voice
        if voice_state is not None:
            link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 'chess')
            emoji = get(ctx.guild.emojis, name="party")
            embed = discord.Embed(
                title="Click en el link para iniciar (BETA)",
                description=f'[{emoji} Iniciar en el canal {ctx.author.voice.channel.name} {emoji}]({link})',
                color=discord.Colour.red(),
            )
            await ctx.send(embed=embed)
        else:
            await ctx.send('**Para usar este comando necesitas unirte a un canal de voz**')

    @commands.command(name="helpac")
    async def helpac(self, ctx):
        voice_state = ctx.message.author.voice
        if voice_state is not None:
            emoji = get(ctx.guild.emojis, name="teemoOk")
            embed = discord.Embed(
                title=f"Comandos disponibles (BETA){emoji} ",
                description=f'\n youtube o yt'
                            f'\n poker'
                            f'\n betrayal'
                            f'\n fishing'
                            f'\n chess',
                color=discord.Colour.dark_magenta(),
            )
            await ctx.send(embed=embed)

        else:
            await ctx.send('**Para usar este comando necesitas unirte a un canal de voz**')

    @commands.command(name="chebo")
    async def check(self, ctx):
        """ Real name of chebo"""
        await ctx.send(f'Chebolin chebo chebo chebo chebo chebo chebo ')

    @commands.command(name="skar")
    async def skar(self, ctx):
        """ skar skar skar"""
        await ctx.send('✂️')

def teardown(bot):
    print('ActivitiesBeta: I am being unloaded!')


def setup(bot):
    bot.add_cog(ActivitiesBeta(bot))
    print('ActivitiesBeta: loaded!')
