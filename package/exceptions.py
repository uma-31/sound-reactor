class InvalidFileType(Exception):
    """無効なファイル形式だったことを知らせる例外クラス"""
    pass


class SoundDataNotFound(Exception):
    """指定された音データが存在しなかったことを知らせる例外クラス"""
    pass


class SoundDataAlreadyExists(Exception):
    """音データが既に存在することを知らせる例外クラス"""
    pass
