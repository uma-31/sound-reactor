from discord import Embed, FFmpegPCMAudio, VoiceClient
from discord.ext import commands
from .data_manage import (
    get_all_sound_data,
    get_sound_file_path,
    initialize,
    regist_sound,
    remove_sound,
    update_description
)


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
        async def sounds(ctx: commands.Context) -> None:
            await self.__on_sounds_command(ctx)

        @self.command()
        async def add(ctx: commands.Context,
                      alias: str) -> None:
            await self.__on_add_command(ctx, alias)

        @self.command()
        async def describe(ctx: commands.Context,
                           alias: str,
                           description: str) -> None:
            await self.__on_describe_command(ctx, alias, description)

        @self.command()
        async def remove(ctx: commands.Context,
                         alias: str) -> None:
            await self.__on_remove_command(ctx, alias)

        @self.command()
        async def play(ctx: commands.Context,
                       alias: str) -> None:
            await self.__on_play_command(ctx, alias)

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

    async def __on_sounds_command(self, ctx: commands.Context) -> None:
        """
        Parameters
        ----------
        ctx : Context
            https://discordpy.readthedocs.io/ja/latest/ext/commands/api.html#discord.ext.commands.Context
        """
        embed = Embed(title='音データ一覧')

        sounds: list[tuple[str, str]] = get_all_sound_data()

        if len(sounds) == 0:
            embed.description = '音データが登録されていません。'

        for sound in sounds:
            embed.add_field(name=sound[0], value=sound[1], inline=False)

        await ctx.send(embed=embed)

    async def __on_add_command(self,
                               ctx: commands.Context,
                               alias: str) -> None:
        """
        Parameters
        ----------
        ctx : Context
            https://discordpy.readthedocs.io/ja/latest/ext/commands/api.html#discord.ext.commands.Context

        alias : str
            登録する音データのエイリアス
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

        try:
            await regist_sound(alias, ctx.message.attachments[0])
        except Exception as e:
            await self.__reply_error_message(ctx, e.args[0])

    async def __on_describe_command(self,
                                    ctx: commands.Context,
                                    alias: str,
                                    description: str) -> None:
        """
        Parameters
        ----------
        ctx : commands.Context
            https://discordpy.readthedocs.io/ja/latest/ext/commands/api.html#discord.ext.commands.Context

        alias : str
            詳細情報を設定する音データのエイリアス

        description : str
            詳細情報
        """
        try:
            update_description(alias, description)
        except Exception as e:
            await self.__reply_error_message(ctx, e.args[0])

    async def __on_remove_command(self,
                                  ctx: commands.Context,
                                  alias: str) -> None:
        """
        Parameters
        ----------
        ctx : Context
            https://discordpy.readthedocs.io/ja/latest/ext/commands/api.html#discord.ext.commands.Context

        alias : str
            削除する音データのエイリアス
        """
        try:
            remove_sound(alias)
        except Exception as e:
            await self.__reply_error_message(ctx, e.args[0])

    async def __on_play_command(self,
                                ctx: commands.Context,
                                alias: str) -> None:
        """
        Parameters
        ----------
        ctx : commands.Context
            https://discordpy.readthedocs.io/ja/latest/ext/commands/api.html#discord.ext.commands.Context

        alias : str
            再生する音データのエイリアス
        """
        if ctx.author.voice is None:  # type: ignore
            await self.__reply_error_message(ctx, 'playコマンドを実行するにはボイスチャンネルに接続してください。')
            return

        try:
            sound_file_path = get_sound_file_path(alias)
        except Exception as e:
            await self.__reply_error_message(ctx, e.args[0])
            return

        voice_client: VoiceClient = await ctx.author.voice.channel.connect()  # type: ignore

        voice_client.play(FFmpegPCMAudio(str(sound_file_path)))

        while voice_client.is_playing():
            pass

        await voice_client.disconnect()  # type: ignore
