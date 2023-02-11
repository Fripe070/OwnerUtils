import discord.abc
from discord.ext import commands

import breadcord
from breadcord.errors import NotAdministratorError


class OwnerUtils(breadcord.module.ModuleCog):
    def __init__(self, module_id: str):
        super().__init__(module_id)
        self.module_settings = self.bot.settings.BreadcordTasks

    @commands.command()
    @commands.is_owner()
    async def sync(self, ctx: commands.Context, guild: discord.abc.Snowflake = None):
        if guild is not None:
            self.bot.tree.copy_global_to(guild=guild)
        await self.bot.tree.sync(guild=guild)
        await ctx.reply("Commands synchronised!")

    @commands.command()
    @commands.is_owner()
    async def stop(self, ctx: commands.Context) -> None:
        if not await self.bot.is_owner(ctx.author):
            raise NotAdministratorError

        self.logger.info("Stopping bot")
        await ctx.reply("Stopping bot", ephemeral=True)
        await self.bot.close()
        exit()


async def setup(bot: breadcord.Bot):
    await bot.add_cog(OwnerUtils("owner_utils"))
