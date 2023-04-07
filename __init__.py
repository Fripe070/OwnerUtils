from typing import Literal

import discord.abc
from discord.ext import commands

import breadcord


class OwnerUtils(breadcord.module.ModuleCog):
    @commands.command()
    @commands.is_owner()
    async def stop(self, ctx: commands.Context) -> None:
        """Stops the bot and the running python process."""
        self.logger.info("Stopping bot")
        await ctx.reply("Stopping bot", ephemeral=True)
        await self.bot.close()
        exit()

    # Based on the sync command by AbstractUmbra
    # https://gist.github.com/AbstractUmbra/a9c188797ae194e592efe05fa129c57f#sync-command-example
    @commands.command()
    @commands.guild_only()
    @commands.is_owner()
    async def sync(
        self,
        ctx: commands.Context,
        guilds: commands.Greedy[discord.Object] = commands.parameter(description="The guilds to sync in"),
        mode: Literal["~", "*", "^", "^*"] | None = commands.parameter(default=None, description="The guilds to sync in"),
    ) -> None:
        """
        Syncs the app command tree.

        Sync options:
        `~`: Syncs the current guild
        `*`: Copies global commands to the current guild
        `^`: Clears guild specific commands in the current guild, or the specified guilds
        Nothing: Syncs globally
        """

        if mode is None and guilds:
            response = await ctx.reply("Syncing app commands in the specified guild(s)...")
            for guild in guilds:
                await ctx.bot.tree.sync(guild=guild)
            await response.edit(content=f"Synced app commands in {len(guilds)} guilds.")

        elif mode == "~":
            response = await ctx.reply("Syncing app commands in the current guild...")
            await ctx.bot.tree.sync(guild=ctx.guild)
            await response.edit(content="Synced app commands in the current guild.")

        elif mode == "*":
            response = await ctx.reply("Copying global app commands to the current guild...")
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            await response.edit(content="Copied and synced global app commands to the current guild.")

        elif mode == "^" and guilds:
            response = await ctx.reply("Clearing guild specific app commands in the specified guilds...")
            for guild in guilds:
                ctx.bot.tree.clear_commands(guild=guild)
                await ctx.bot.tree.sync(guild=guild)
            await response.edit(content="Cleared guild specific app commands in the specified guilds.")

        elif mode == "^":
            response = await ctx.reply("Clearing guild specific app commands in the current guild...")
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            await response.edit(content="Cleared guild specific app commands in the current guild.")

        else:
            response = await ctx.reply("Syncing app commands globally...")
            await ctx.bot.tree.sync()
            await response.edit(content="Synced app commands globally.")



async def setup(bot: breadcord.Bot):
    await bot.add_cog(OwnerUtils("owner_utils"))
