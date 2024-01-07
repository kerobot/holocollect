import urllib.request
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class MongoSettings(BaseSettings):
    """
    MongoDBの設定を管理するクラス
    
    Args:
        uri (str): MongoDBの接続URI
        database (str): 使用するデータベース名
        model_config (SettingsConfigDict): モデルの設定辞書
    """
    uri: str
    database: str
    model_config = SettingsConfigDict(env_file=".env", env_prefix='mongo_')

class YoutubeSettings(BaseSettings):
    """
    YouTubeの設定を管理するクラス

    Args:
        api_key (str): YouTube Data APIのAPIキー
        api_service_name (str): YouTube Data APIのサービス名
        api_version (str): YouTube Data APIのバージョン
        url_pattern (str): YouTubeのURLパターン
        model_config (SettingsConfigDict): モデルの設定辞書
    """
    api_key: str
    api_service_name: str
    api_version: str
    url_pattern: str
    model_config = SettingsConfigDict(env_file=".env", env_prefix='youtube_')

class HoloduleSettings(BaseSettings):
    """
    Holoduleの設定を管理するクラス

    Args:
        url (str): HoloduleのURL
        model_config (SettingsConfigDict): モデルの設定辞書
    """
    url: str
    model_config = SettingsConfigDict(env_file=".env", env_prefix='holodule_')

    async def check_holodule_url(self) -> bool:
        """
        HoloduleのURLが有効かどうかを確認する関数

        Returns:
            bool: URLが有効かどうか
        """
        return await self.__check_url(self.url)

    async def __check_url(self, url: str) -> bool:
        """
        URLが有効かどうかを確認する関数

        Args:
            url (str): 確認するURL

        Returns:
            bool: URLが有効かどうか
        """
        try:
            async with urllib.request.urlopen(url) as response:
                return True
        except Exception:
            return False

@lru_cache
def get_mongo_settings() -> MongoSettings:
    """
    キャッシュしたMongoDBの設定を取得する関数

    Returns:
        MongoSettings: MongoDBの設定
    """
    return MongoSettings()

@lru_cache
def get_youtube_settings() -> YoutubeSettings:
    """
    キャッシュしたYoutubeの設定を取得する関数

    Returns:
        YoutubeSettings: Youtubeの設定
    """
    return YoutubeSettings()

@lru_cache
def get_holodule_settings() -> HoloduleSettings:
    """
    キャッシュしたホロジュールの設定を取得する関数

    Returns:
        HoloduleSettings: ホロジュールの設定
    """
    return HoloduleSettings()
