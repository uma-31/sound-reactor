import sqlite3

from discord import Attachment
from pathlib import Path
from .exceptions import InvalidFileType, SoundDataNotFound


VALID_FILE_EXTENSIONS = ['wav', 'mp3']

PROJECT_ROOT = Path(__file__).parent.parent

DB_FILE = PROJECT_ROOT / 'data.db'
DATA_DIR = PROJECT_ROOT / 'data/'


def initialize_database() -> None:
    """データベースを初期化する"""
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    cur.execute('''CREATE TABLE sounds
                   (alias text primary key, description text)''')

    con.commit()
    con.close()


async def regist_sound(alias: str,
                       sound_data: Attachment,
                       description: str = 'no description') -> None:
    """
    音データを登録する

    ...

    Parameters
    ----------
    alias : str
        登録するエイリアス

    sound_data : discord.Attachment
        ディスコードのメッセージに添付された音声データ

    description : str, default='no description'
        音データの詳細情報

    Raises
    ----------
    InvalidFileType
        無効なファイル形式だった場合に発生する
    """
    file_extension: str = sound_data.filename.split('.')[-1]

    if file_extension not in VALID_FILE_EXTENSIONS:
        raise InvalidFileType(f'{file_extension}形式のファイルには対応していません。')

    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    cur.execute('''INSERT INTO sounds VALUES(:alias :description)''',
                {'alias': alias, 'description': description})

    con.commit()
    con.close()

    await sound_data.save(str(DATA_DIR / f'{alias}.{file_extension}'))


def remove_sound(alias: str) -> None:
    """
    登録されている音ファイルを削除する

    ...

    Parameters
    ----------
    alias : str
        削除する音データのエイリアス
    """
    valid_extensions_re = '|'.join(VALID_FILE_EXTENSIONS)

    target_sound_files = list(DATA_DIR.glob(
        f'{alias}.({valid_extensions_re})'))

    if len(target_sound_files) == 0:
        raise SoundDataNotFound(f'音声データ{alias}は存在しません。')

    target_sound_files[0].unlink()

    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    cur.execute('''DELETE FROM sounds WHERE alias=:alias''',
                {'alias': alias})

    con.commit()
    con.close()
