import random
from pathlib import Path
from typing import Any

import yaml
from discord.ext import commands
from loguru import logger

from tux.bot import Tux
from tux.ui.embeds import EmbedCreator


class GodSpeak(commands.Cog):
    def __init__(self, bot: Tux) -> None:
        self.bot = bot
        self.vocab = self.load_vocab()

    def load_vocab(self) -> list[str]:
        vocab_path = Path(__file__).parent / "vocab.yml"

        if not vocab_path.exists():
            logger.error(f"vocab.yml not found at {vocab_path.resolve()}")
            return []

        with vocab_path.open(encoding="utf-8") as f:
            raw_data: Any = yaml.safe_load(f)

        if not isinstance(raw_data, list):
            logger.error("vocab.yml must be a list.")
            return []

        return [str(item) for item in raw_data]  # type: ignore (idk why it gives me an error but i don't care so)

    @commands.hybrid_command(name="godspeak", aliases=["gs"], description="Receive a divine message.")
    @commands.guild_only()
    async def godspeak(self, ctx: commands.Context[Tux]) -> None:
        if not self.vocab:
            logger.error("No vocabulary check `vocab.yml`.")
            return

        wordcount = random.randint(10, 100)  # change this if you want longer messages
        wordspicked = random.choices(self.vocab, k=wordcount)
        message = " ".join(wordspicked)

        embed = EmbedCreator.create_embed(
            bot=self.bot,
            embed_type=EmbedCreator.NOTE,
            title="God's Message",
            description=message,
        )
        await ctx.send(embed=embed)


async def setup(bot: Tux) -> None:
    await bot.add_cog(GodSpeak(bot))
