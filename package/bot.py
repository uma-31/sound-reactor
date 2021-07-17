from argparse import ArgumentParser
from discord import Embed
from discord.errors import InvalidArgument
from package.exceptions import InvalidFileType
from discord.ext import commands
from .data_manage import regist_sound, remove_sound


class SoundReactor(commands.Bot):
    """BOT本体"""

    def __init__(self, **config) -> None:
        """
        Parameters
        ----------
        token : str
            トークン

        config : dict[str, Any]
            各種設定
        """
        pass
