from discord import Embed
from package.exceptions import InvalidFileType
from discord.ext import commands
from .data_manage import initialize, is_sound_exists, regist_sound


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
        super().__init__(
            command_prefix='.' if 'prefix' not in config else config['prefix'])

        initialize()

        @self.command()
        async def add(ctx: commands.Context,
                      alias: str) -> None:
            await self.__on_add_command(ctx, alias)

    async def __reply_error_message(self,
                                    ctx: commands.Context,
                                    message: str):
        """
        エラーメッセージを返信する

        ...

        Parameters
        ----------
        ctx : Context
            https://discordpy.readthedocs.io/ja/latest/ext/commands/api.html#discord.ext.commands.Context

        message : str
            送信するメッセージ
        """
        embed = Embed(title='Error!',
                      description=message,
                      color=0xfffc66)

        await ctx.send(embed=embed)

    async def __on_add_command(self,
                               ctx: commands.Context,
                               alias: str) -> None:
        """
        Parameters
        ----------
        ctx : Context
            https://discordpy.readthedocs.io/ja/latest/ext/commands/api.html#discord.ext.commands.Context

        *args : list[str]
            引数のリスト
        """
        if ctx.message is None:
            await self.__reply_error_message(ctx, '予期せぬエラーが発生しました。')
            return

        n_attachments = len(ctx.message.attachments)

        if n_attachments == 0:
            await self.__reply_error_message(ctx, 'ファイルが添付されていません！')
            return
        elif n_attachments > 1:
            await self.__reply_error_message(ctx, 'addコマンドで添付できるファイルは1つです。')
            return

        if is_sound_exists(alias):
            await self.__reply_error_message(ctx, f'{alias}は既に登録されています。')
            return

        try:
            await regist_sound(alias, ctx.message.attachments[0])
        except InvalidFileType as e:
            await self.__reply_error_message(ctx, e.args[0])
            return
