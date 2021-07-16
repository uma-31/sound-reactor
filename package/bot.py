from discord.ext import commands


class SoundReactor(commands.Bot):
    """BOT本体"""

    def __init__(self, token: str, **config) -> None:
        """
        Parameters
        ----------
        token : str
            トークン

        config : dict[str, Any]
            各種設定
        """
        pass
