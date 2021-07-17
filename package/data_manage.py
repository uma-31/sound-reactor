import sqlite3

from discord import Attachment
from pathlib import Path
from .exceptions import InvalidFileType, SoundDataAlreadyExists, SoundDataNotFound


VALID_FILE_EXTENSIONS = ['wav', 'mp3']

PROJECT_ROOT = Path(__file__).parent.parent

DB_FILE = PROJECT_ROOT / 'data.db'
DATA_DIR = PROJECT_ROOT / 'data/'


def initialize() -> None:
    """データの保存場所を確保する"""
    if not DB_FILE.is_file():
        con = sqlite3.connect(DB_FILE)
        cur = con.cursor()

        cur.execute('''CREATE TABLE sounds
                    (alias text primary key, description text)''')

        con.commit()
        con.close()

    if not DATA_DIR.is_dir():
        DATA_DIR.mkdir()


def get_all_sound_data() -> list[tuple[str, str]]:
    """
    登録された音データの情報を全て取得する

    Returns
    ----------
    list[tuple[str, str]]
        (エイリアス, 詳細情報)の組のリスト

    Note
    ----------
    ここで取得できるデータはデータベースに保存されているものであり，
    音データそのものは含まれないことに注意してください．
    """
    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    cur.execute('''SELECT alias, description FROM sounds''')

    data = cur.fetchall()

    con.close()

    return data


def is_sound_exists(alias: str) -> bool:
    """
    エイリアスから音データの存在を確認する

    ...

    Parameters
    ----------
    alias : str
        存在を確認したい音データのエイリアス

    Returns
    ----------
    bool
        指定されたエイリアスで登録された音データが
        存在するかどうか
    """

    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    cur.execute('''SELECT * FROM sounds WHERE alias=:alias''',
                {'alias': alias})

    data = cur.fetchall()

    con.close()

    return len(data) == 1


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
    SoundDataAlreadyExists
        指定されたエイリアスが既に登録されていた場合に発生する

    InvalidFileType
        無効なファイル形式だった場合に発生する
    """
    if is_sound_exists(alias):
        raise SoundDataAlreadyExists(f'{alias}は既に登録されています。')

    file_extension: str = sound_data.filename.split('.')[-1]

    if file_extension not in VALID_FILE_EXTENSIONS:
        raise InvalidFileType(f'{file_extension}形式のファイルには対応していません。')

    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    cur.execute('''INSERT INTO sounds VALUES(:alias, :description)''',
                {'alias': alias, 'description': description})

    con.commit()
    con.close()

    await sound_data.save(str(DATA_DIR / f'{alias}.{file_extension}'))


def remove_sound(alias: str) -> None:
    """
    登録されている音データを削除する

    ...

    Parameters
    ----------
    alias : str
        削除する音データのエイリアス

    Raises
    ----------
    SoundDataNotFound
        指定された音データが存在しなかった場合に発生する
    """
    if not is_sound_exists(alias):
        raise SoundDataNotFound(f'{alias}は登録されていません。')

    target_sound_files = list(DATA_DIR.glob(f'{alias}.*'))
    target_sound_files[0].unlink()

    con = sqlite3.connect(DB_FILE)
    cur = con.cursor()

    cur.execute('''DELETE FROM sounds WHERE alias=:alias''',
                {'alias': alias})

    con.commit()
    con.close()
