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

from collections import namedtuple
from datetime import  datetime as dt

import discord
import requests
from discord.ext import commands, tasks

from models.base import session
from models.giveaways import Giveaways


class Giveaway(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.scan_giveaways.start()

    @commands.command(name="freegames")
    async def freegames(self, ctx):
        """"Gives you a full list of free games (please use only on spam channels)"""

        result = session.query(Giveaways).order_by(Giveaways.published_date)
        for row in result:
            #print(row)
            descripcion = f""" {row.title}
                           **Desde**: {row.published_date}
                           **Hasta **: {row.end_date}
                           **Precio **: ~~{row.worth}~~ **free**
                           **Enlace **: [Reclamalo Aqui!]({row.open_giveaway_url})
                           **Plataformas **: {row.platforms}
                           """
            embed = discord.Embed(title=row.title, description=descripcion)  # ,color=Hex code
            print(row.title)
                    # print(response.json())
            embed.add_field(name="instrucciones", value=row.instructions)

            embed.set_thumbnail(url=row.thumbnail)
            embed.set_footer(text=f"Status: {row.status}")

            await ctx.send(embed=embed)


    async def publish_latest_giveaway(self, giveaway:Giveaways):

        descripcion = f""" {giveaway.title}
                       **Desde**: {giveaway.published_date}
                       **Hasta **: {giveaway.end_date}
                       **Precio **: ~~${giveaway.worth}~~ **free**
                       **Enlace **: [Reclamalo Aqui!]({giveaway.open_giveaway_url})
                       **Plataformas **: {giveaway.platforms}
                       """
        embed = discord.Embed(title=giveaway.title, description=descripcion)  # ,color=Hex code
        print(giveaway.title)
        #print(response.json())
        embed.add_field(name="Instrucciones", value=giveaway.instructions)

        #embed.set_thumbnail(url=giveaway.thumbnail)
        embed.set_image(url=giveaway.thumbnail)
        embed.set_footer(text=f"Status: {giveaway.status}")

        for guild in self.bot.guilds:
            gui = self.bot.get_guild(guild.id)
            if gui is None:
                print(type(guild), "Guild not found")
            else:
                #get che channele
                channel = gui.system_channel
                await channel.send(embed=embed)

    @tasks.loop(seconds=14400)
    async def scan_giveaways(self):
        """
        Responses
        200: Success
        201: No active giveaways available at the moment, please try again later.
        404: Object not found: Giveaway or endpoint not found.
        500: Something wrong on our end (unexpected server errors).
        """
        #wait until the bot is ready  for getting data  from discord api
        await self.bot.wait_until_ready()

        #look for  data in api
        response  = requests.get("https://www.gamerpower.com/api/giveaways")
        if response.status_code == 200:
            """ save the users roles """

            for game in response.json():
                #print(game)
                result = session.query(Giveaways).filter(Giveaways.id==game["id"]).count()
                if result == 0 :
                    giveaway =  namedtuple("ObjectName", game.keys())(*game.values())
                    worth = str(giveaway.worth)
                    if giveaway.worth == "N/A":
                        worth = str(0.0)
                    worth = float(worth.replace('$',''))
                    description = giveaway.description.replace('"',"")
                    instructions = giveaway.instructions.replace('"',"")
                    published_date = None
                    end_date = None
                    if giveaway.published_date != "N/A":
                        published_date = dt.strptime(giveaway.published_date, "%Y-%m-%d %H:%M:%S")
                    if giveaway.end_date != "N/A":
                        end_date = dt.strptime(giveaway.end_date,"%Y-%m-%d %H:%M:%S")

                    give = Giveaways(giveaway.id,giveaway.title,worth,giveaway.thumbnail,
                                    giveaway.image,description,instructions,giveaway.open_giveaway_url,
                                    published_date,giveaway.type,giveaway.platforms,end_date,giveaway.users,
                                    giveaway.status,giveaway.gamerpower_url,giveaway.open_giveaway)
                    session.add(give)

                    #send game to all the guilds
                    await self.publish_latest_giveaway(give)
            session.commit()
        elif response.status_code == 201:
            print('No active giveaways available at the moment, please try again later.')
        elif response.status_code == 404:
            print('Object not found: Giveaway or endpoint not found.')
        elif response.status_code == 500:
            print('Something wrong on our end (unexpected server errors).')


def teardown(bot):
    print('Giveaway: I am being unloaded!')

def setup(bot):
    bot.add_cog(Giveaway(bot))
    print('Giveaway: loaded!')
