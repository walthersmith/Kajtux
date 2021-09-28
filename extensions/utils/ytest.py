import discord
from aiohttp import ClientSession
from discord import member
from discord.ext import commands
import requests
from discord.ext.commands import BotMissingPermissions
from discord.http import Route
from discord.utils import get

from extensions.utils.erros import InvalidChannelID


class ActivityLink:
    """
    Holds three variations of the invite link. Without any attributes, returns complete http link (https://discord.gg/invite_code)
    ----------
    Attributes
    - short_link
        Returns (discord.gg/invite_code)
    - raw_code
        Returns (raw_code)
    """

    def __init__(self, inviteCode: str):
        self.raw_code = inviteCode
        self.short_link = f"discord.gg/{inviteCode}"

    def __repr__(self):
        return f"https://discord.gg/{self.raw_code}"


class YtTogether(commands.Cog):
    """Utilities that provide pseudo-RNG."""

    def __init__(self, bot):
        self.bot = bot
        self.debug = True

    @commands.command(name="ytt")
    async def ytt(self, ctx):
        mem = ctx.guild.get_member(ctx.message.author.id)
        voice_state = mem.voice
        if voice_state is not None:
            channel_id = mem.voice.channel.id
            _DATA = {
                'max_age': 86400,
                'max_uses': 0,
                'target_application_id': 755600276941176913,  # youtube-together
                'target_type': 2,
                'temporary': False,
                'validate': None
            }
            try:
                result = await self.bot.http.request(
                    Route("POST", f"/channels/{channel_id}/invites"), json=_DATA
                )

                link = ActivityLink(result['code'])
                emoji = get(ctx.guild.emojis, name="party")
                embed = discord.Embed(
                    title="Click the link to start YouTube",
                    description=f'[{emoji} Start in channel: {mem.voice.channel.name} {emoji}]({link})',
                    color=discord.Colour.red(),
                )

                await ctx.send(embed=embed)
            except Exception as e:
                if self.debug:
                    async with ClientSession() as session:
                        async with session.post(f"https://discord.com/api/v8/channels/{channel_id}/invites",
                                                json=_DATA,
                                                headers={
                                                    'Authorization': f'Bot {self.bot.http.token}',
                                                    'Content-Type': 'application/json'
                                                }
                                                ) as resp:
                            result = await resp.json()
                    print('\033[95m' + '\033[1m' + '[DEBUG] (discord-together) Response Output:\n' + '\033[0m' + str(
                        result))

                    print(e)

        else:
            await ctx.send('You need to join to a voice channel first!')


def teardown(bot):
    print('YtTogether: I am being unloaded!')


def setup(bot):
    bot.add_cog(YtTogether(bot))
    print('YtTogether: loaded!')
