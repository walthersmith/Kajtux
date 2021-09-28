"""
======================= START OF LICENSE NOTICE =======================
  Copyright (C) 2021 walther smith franco otero. All Rights Reserved

  NO WARRANTY. THE PRODUCT IS PROVIDED BY DEVELOPER "AS IS" AND ANY
  EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
  IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR
  PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL DEVELOPER BE LIABLE FOR
  ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
  DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE
  GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
  INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
  IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR
  OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THE PRODUCT, EVEN
  IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
======================== END OF LICENSE NOTICE ========================
  Primary Author: Walther smith franco otero

"""
import datetime
import itertools

import pygit2
from collections import Counter

import discord
import pkg_resources
import psutil
from discord.errors import Forbidden, HTTPException
from discord.ext import commands, tasks

from models.GenericData import GenericData
from models.user_warnings import Users_warnings
from models.users import Users
from models.users_roles import Users_roles
from models.warning_config import Warning_config
from models.warning_log import Warning_log
from extensions.utils import time
from models.base import session, update, Session
from models.jail import Jail


class Moderation(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process()
        self.uptime = datetime.datetime.utcnow()
        self.verify_jail.start()

    @commands.command(name='addrole')
    @commands.has_permissions(administrator=True)
    async def add_role(self, ctx, member: discord.Member = None, role: discord.Role = None):
        """give a role to a specific user ex: addrole @user"""
        if member is not None and role is not None:
            if role.position > ctx.author.top_role.position:
                return await ctx.send(f'**:x: | That role is above your top role {member.top_role.name}!!**')
            if role in member.roles:
                return await ctx.send(f'the user {member.display_name} has already that role')
            else:
                try:
                    await member.add_roles(role)  # adds role if not already has it
                    await ctx.send(f'Role  {role} added to {member.mention}')
                except discord.errors.Forbidden as e:
                    print(f"Forbidden: {e.text}")
                    if isinstance(e, Forbidden):
                        await ctx.send(f'**:x: | Kajtux do not have permission to asign the role ({role.name})**')
                except HTTPException as x:
                    await ctx.send(f'**:x: | Adding roles failed.**')
                    print(f"HTTPException: {x.text}")
        else:
            await ctx.send(f'please specify the user and role to asig ')
            await ctx.send(f'ej: addrole @username @roleName')

    @commands.command(name="warn", pass_context=True)
    @commands.has_permissions(manage_roles=True)  # Check if the user executing the command can manage roles
    @commands.has_permissions(administrator=True)
    async def warn(self, ctx, member: discord.Member = None, reason='none', *args):

        if GenericData().get_cnt_warning_config(ctx.message.guild.id) > 0:
            """ registra una advertencia al usuario"""

            if ctx.author.top_role.position == member.top_role.position and ctx.guild.owner.id != ctx.author.id:
                return await ctx.send(f"I can't warn this user: {member.mention} you  have the same rol level ")

            print(f"Guild:id {ctx.message.guild.id}")
            print(f"{member.display_name} : id {member.id}")

            # save user
            if session.query(Users).filter_by(id=member.id).count() == 0:
                user = Users()
                user.id = member.id
                user.username = member.display_name
                session.add(user)
                session.commit()

            if session.query(Users_warnings).filter_by(user_id=member.id, guild_id=ctx.message.guild.id).count() == 0:
                user_war = Users_warnings()
                user_war.user_id = member.id
                user_war.guild_id = ctx.message.guild.id
                user_war.warnings = 0
                session.add(user_war)
                session.commit()

            warning_log = Warning_log()
            warning_log.user_id = member.id
            warning_log.guild_id = ctx.message.guild.id
            warning_log.reason = reason
            session.add(warning_log)

            update(Users_warnings).where(Users_warnings.user_id == member.id,
                                         Users_warnings.guild_id == ctx.message.guild.id).values(
                {Users_warnings.warnings: Users_warnings.warnings + 1})
            session.commit()

            await ctx.send(f'User: {member.mention} has been warned ')

            result = session.query(Users_warnings, Warning_config) \
                .filter(Users_warnings.guild_id == Warning_config.guild_id,
                        Users_warnings.warnings >= Warning_config.limit, Users_warnings.user_id == member.id).count()

            if result >= 0:
                await self.delete_and_save_roles(ctx, member)

        else:
            await ctx.send(f'**warns has not been configured yet for this server** use: "warnsetup" ')

    @commands.command(name="mute")
    @commands.has_permissions(administrator=True)
    async def jail_now(self, ctx, member: discord.Member = None, jail_time=0):
        """ find and delete all roles of a specific user then send this user to the jail
             ex: mute @user """
        await self.register_user(ctx, member)
        await self.delete_and_save_roles(ctx, member, jail_time)

    @commands.command(name="warnsetup")
    @commands.has_permissions(administrator=True)
    async def warnsetup(self, ctx):
        """help you to configure warns in your server (BETA)"""
        await ctx.send(f'**Great then just answer the  following questions  to configure the warns/jail config**')

        def check_tch_mention(m):
            return len(m.channel_mentions) != 0 and m.author == ctx.author and m.channel == ctx.channel

        def check_vch_mention(m):
            return len(m.raw_role_mentions) != 0 and m.author == ctx.author and m.channel == ctx.channel

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        await ctx.send("Please give me the warnings limit")

        message = await self.bot.wait_for('message', check=check, timeout=10)
        warning_limit = message.content
        print("warnings limit", warning_limit)

        await ctx.send("Please mention  the muted/jail text channel")

        # Wait for a response
        jail_ch_channel = 0
        response = await self.bot.wait_for('message', check=check_tch_mention, timeout=10)
        if isinstance(response.channel_mentions[0], discord.TextChannel):
            jail_ch_channel = response.channel_mentions[0].id
            print(jail_ch_channel)

        await ctx.send("Please give the muted/jail Rol")

        response = await self.bot.wait_for('message', check=check_vch_mention, timeout=10)
        muted_rol_id = response.raw_role_mentions[0]
        print("muted roll id : ", muted_rol_id)

        await ctx.send("Please give me  the ID of voice muted/jail channel")

        message = await self.bot.wait_for('message', check=check, timeout=10)
        jail_vch_id = message.content
        print("voice channel id :", jail_vch_id)

        await ctx.send("how many minutes of punishment?")
        message = await self.bot.wait_for('message', check=check, timeout=10)
        jail_time = message.content
        print("voice channel id :", jail_time)

        session.query(Warning_config).filter(Warning_config.guild_id == ctx.message.guild.id).delete()

        warning_config = Warning_config()
        warning_config.guild_id = ctx.message.guild.id
        warning_config.limit = warning_limit
        warning_config.jail_role = muted_rol_id
        warning_config.jail_time = jail_time
        warning_config.voice_ch_id = jail_vch_id
        warning_config.text_ch_id = jail_ch_channel
        session.add(warning_config)
        session.commit()

        description = f""" Saved configurations: 
                           **warning limit **:     {warning_limit}
                           **Jail time**:          {jail_time}
                           **Muted/jail Role: **:  {muted_rol_id}
                           **Jail text channel**:  {jail_ch_channel}
                           **Jail voice channel**: {jail_vch_id}
                      """
        embed = discord.Embed(title="Warnings configurations", description=description)  # ,color=Hex code
        embed.set_footer(text=f" :) ")

        await ctx.send(embed=embed)

    async def delete_roles(self, user_id=None, guild_id=None):
        result = session.query(Users_roles).filter(Users_roles.user_id == user_id,
                                                   Users_roles.guild_id == guild_id).delete()

    async def delete_and_save_roles(self, ctx, member: discord.Member = None, jail_time=0):
        # guardamos los roles del usuario.
        ses = session  # Session()
        await self.roles(ctx, member)
        print(f'Ahora se quitaran los roles ')
        await member.remove_roles()
        # for role in member.roles:
        #     if role.is_default() == False:
        #         print(f"removing: {role.id}: {role.name}")
        #         await member.remove_roles(role)

        # we look for warning configs
        conf = ses.query(Warning_config).filter_by(guild_id=ctx.message.guild.id).first()
        if conf is None:
            return None
        if jail_time == 0:
            jail_time = conf.jail_time
            await self.jail_user(ctx, member, conf.jail_role, conf.voice_ch_id, conf.jail_time)

        # asignamos la hora mas los minutos a estar en la carcel
        actual_time = datetime.datetime.now()
        seconds = (60 * jail_time)
        jail_end_time = actual_time + datetime.timedelta(seconds=seconds)
        print(f"{jail_end_time} - {seconds} - {jail_time}")

        jail = Jail()
        jail.user_id = member.id
        jail.guild_id = ctx.message.guild.id
        jail.end_date = jail_end_time
        ses.add(jail)
        ses.commit()
        ses.close()

    async def jail_user(self, ctx, member: discord.Member = None, jail_role_id=None, jail_vch_id=None, jail_time=None):
        # voice channel
        voice_channel_id = jail_vch_id
        if voice_channel_id != 0:
            voice_channel = discord.utils.get(ctx.guild.voice_channels, id=voice_channel_id)
            voice_state = member.voice
            if voice_state is not None:
                await member.move_to(channel=voice_channel)
                await member.edit(mute=True)

        print(f"Asignando Jail Role:  {jail_role_id}")
        role = discord.utils.get(ctx.guild.roles, id=jail_role_id)
        await member.add_roles(role)  # adds role if not already has it

        await ctx.send(f'{member.mention} is now on jail  for {jail_time} minutes')

    async def roles(self, ctx, member: discord.Member = None):
        """ save the users roles """
        print(f"Guild:id {ctx.message.guild.id}")
        print(f"{member.display_name} : id {member.id}")

        result = session.query(Users).filter(Users.id == member.id).first()
        if result is None:
            # Save user
            user = Users()
            user.id = member.id
            user.username = member.display_name
            session.add(user)
            session.commit()

        # delete users_roles from db
        await  self.delete_roles(user_id=member.id, guild_id=ctx.message.guild.id)

        # save user roles
        for role in member.roles:
            if role.is_default() == False and role.is_premium_subscriber() == False:
                result = session.query(Users_roles).filter(Users_roles.guild_id == ctx.message.guild.id,
                                                           Users_roles.user_id == member.id,
                                                           Users_roles.id_role == role.id).count()
                if result == 0:
                    print(f"Saving role: {role.id}: {role.name}")
                    user_rol = Users_roles()
                    user_rol.user_id = member.id
                    user_rol.guild_id = ctx.message.guild.id
                    user_rol.id_role = role.id
                    user_rol.role_name = role.name
                    session.add(user_rol)
                    session.commit()
                    print("Removing role: ", role)
                    await member.remove_roles(role)

    async def register_user(self, ctx, member: discord.Member = None):

        users = session.query(Users).filter_by(id=member.id).first()
        if users is None:
            user = Users()
            user.id = member.id
            user.username = member.display_name
            session.add(user)
            session.commit()
        session.close()
        # await self.roles(ctx,member)

    @commands.command(name="unjail")
    @commands.bot_has_permissions(administrator=True)
    async def unjail(self, ctx, member: discord.Member = None):
        """Restore it all the roles of an user and take it out from the jail """
        result = session.query(Jail).filter(Jail.user_id == member.id, Jail.guild_id == ctx.message.guild.id).count()
        if result > 0:
            await self.unjail_user(user_id=member.id, guild_id=ctx.message.guild.id)
            session.query(Jail).filter(Jail.user_id == member.id, Jail.guild_id == ctx.message.guild.id).delete()
            await ctx.send(f'{member.mention} is now free!!')
        else:
            await ctx.send(f'{member.mention} is not on jail ')

    async def unjail_user(self, user_id, guild_id):
        # crear los objetos
        print(f"guild {guild_id}")
        print(f"user {user_id}")
        guild = self.bot.get_guild(guild_id)
        if guild is None:
            print(type(guild), "guild not found")
        else:
            print(type(guild), "guild  found")
            member = guild.get_member(user_id)

            # eliminar rol de muted
            print(f"removing roles  from {member.display_name}")
            roles = [role for role in member.roles if
                     role.is_default() == False and role.is_premium_subscriber() == False]
            await member.remove_roles(*roles)

            # buscamos los roles guardados
            result = session.query(Users_roles.id_role, Users_roles.role_name).filter(Users_roles.user_id == user_id,
                                                                                      Users_roles.guild_id == guild_id)
            if result is not None:
                for row in result:
                    # restore the users role
                    print(f"restoring role {row[1]}")
                    role = guild.get_role(row[0])
                    await member.add_roles(role)
                    voice_state = member.voice
                    if voice_state is not None:
                        await member.edit(mute=False)
                jail_id_channel = session.query(Warning_config.text_ch_id).filter(
                    Warning_config.guild_id == guild.id).first()
                print('Jail ID: ', jail_id_channel[0])
                jail_channel = guild.get_channel(channel_id=jail_id_channel[0])
                print(type(jail_channel))
                if jail_channel is not None:
                    await jail_channel.send(f'{member.mention} is now free!!')
                else:
                    print("Channel not Found!")

    @tasks.loop(seconds=2)
    async def verify_jail(self):
        """
        Read the jail table and verify  each row
          compare  end date to actual date an
          delete row if  end_date is < to actual date """

        # wait until the bot is ready  for getting data  from discord api
        await self.bot.wait_until_ready()

        actual_time = datetime.datetime.now()
        recluses = session.query(Jail).all()
        if recluses is not None:
            for recluse in recluses:
                jail_end_date = datetime.datetime.fromisoformat(str(recluse.end_date))
                print(f"{recluse.user_id}, {recluse.guild_id}, {recluse.end_date} ac:{actual_time}")
                if actual_time > jail_end_date:
                    print(f"releasing prisoner {recluse.user.username}")
                    session.delete(recluse)
                    await self.unjail_user(user_id=recluse.user_id, guild_id=recluse.guild_id)
            session.commit()

    async def get_or_fetch_member(self, guild, member_id):
        """Looks up a member in cache or fetches if not found.
        Parameters
        -----------
        guild: Guild
            The guild to look in.
        member_id: int
            The member ID to search for.
        Returns
        ---------
        Optional[Member]
            The member or None if not found.
        """

        if guild is None:
            print(type(guild), "guild not found")
        else:
            print(type(guild), "guild  found")
            member = guild.get_member(member_id)

        shard = self.bot.get_shard(guild.shard_id)
        if shard.is_ws_ratelimited():
            try:
                member = await guild.fetch_member(member_id)
            except discord.HTTPException:
                return None
            else:
                return member

        members = await guild.query_members(limit=1, user_ids=[member_id], cache=True)
        if not members:
            return None
        return members[0]

    def format_commit(self, commit):
        short, _, _ = commit.message.partition('\n')
        short_sha2 = commit.hex[0:6]
        commit_tz = datetime.timezone(datetime.timedelta(minutes=commit.commit_time_offset))
        commit_time = datetime.datetime.fromtimestamp(commit.commit_time).astimezone(commit_tz)

        # [`hash`](url) message (offset)
        offset = time.human_timedelta(commit_time.astimezone(datetime.timezone.utc).replace(tzinfo=None), accuracy=1)
        return f'[`{short_sha2}`](https://github.com/walthersmith/kajtux/commit/{commit.hex}) {short} ({offset})'

    def get_last_commits(self, count=3):
        repo = pygit2.Repository('.git')
        commits = list(itertools.islice(repo.walk(repo.head.target, pygit2.GIT_SORT_TOPOLOGICAL), count))
        return '\n'.join(self.format_commit(c) for c in commits)

    def get_bot_uptime(self, *, brief=False):
        return time.human_timedelta(self.uptime, accuracy=None, brief=brief, suffix=False)

    @commands.command()
    async def uptime(self, ctx):
        """Tells you how long the bot has been up for."""
        await ctx.send(f'Uptime: **{self.get_bot_uptime()}**')

    @commands.command()
    async def about(self, ctx):
        """Tells you information about the bot itself."""

        revision = self.get_last_commits()
        embed = discord.Embed(description='Latest Changes:\n' + revision)
        embed.title = 'Official Bot Server Invite'
        embed.url = 'https://discord.gg/wNj2jgCWDz'
        embed.colour = discord.Colour.blurple()

        # To properly cache myself, I need to use the bot support server.
        support_guild = self.bot.get_guild(861783696134111262)
        owner = await self.get_or_fetch_member(support_guild, self.bot.owner_id)
        embed.set_author(name=str(owner))

        # statistics
        total_members = 0
        total_unique = len(self.bot.users)

        text = 0
        voice = 0
        guilds = 0
        for guild in self.bot.guilds:
            guilds += 1
            if guild.unavailable:
                continue

            total_members += guild.member_count
            for channel in guild.channels:
                if isinstance(channel, discord.TextChannel):
                    text += 1
                elif isinstance(channel, discord.VoiceChannel):
                    voice += 1

        embed.add_field(name='Members', value=f'{total_members} total\n{total_unique} unique')
        embed.add_field(name='Channels', value=f'{text + voice} total\n{text} text\n{voice} voice')

        memory_usage = self.process.memory_full_info().uss / 1024 ** 2
        cpu_usage = self.process.cpu_percent() / psutil.cpu_count()
        embed.add_field(name='Process', value=f'{memory_usage:.2f} MiB\n{cpu_usage:.2f}% CPU')

        version = pkg_resources.get_distribution('discord.py').version
        embed.add_field(name='Guilds', value=guilds)
        embed.add_field(name='Commands Run', value=sum(self.bot.command_stats.values()))
        embed.add_field(name='Uptime', value=self.get_bot_uptime(brief=True))
        embed.set_footer(text=f'Made with discord.py v{version}', icon_url='http://i.imgur.com/5BFecvA.png')
        embed.timestamp = datetime.datetime.utcnow()
        await ctx.send(embed=embed)


def teardown(bot):
    print('Moderation: I am being unloaded!')


def setup(bot):
    if not hasattr(bot, 'command_stats'):
        bot.command_stats = Counter()
    bot.add_cog(Moderation(bot))
    print('Giveaway: loaded!')
