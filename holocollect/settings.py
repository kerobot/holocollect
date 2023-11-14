import os
import urllib.request
from dotenv import load_dotenv
from logging import getLogger

class Settings:
    """
    設定情報を保持するクラス
    """
    def __init__(self, env_path: str) -> None:
        """
        Settingsクラスのインスタンスを生成する
        
        Args:
            env_path (str): .envファイルのパス
        
        Raises:
            ValueError: .envファイルの読み込みに失敗した場合
            ValueError: 環境変数が設定されていない場合
        """
        # Logger 関連
        self._logger = getLogger(__name__)
        # env 関連
        self.env_path: str = env_path
        self.__load_env()
        self.__holodule_url: str = self.__get_env("HOLODULE_URL")
        self.__api_key: str = self.__get_env("API_KEY")
        self.__api_service_name: str = self.__get_env("API_SERVICE_NAME")
        self.__api_version: str = self.__get_env("API_VERSION")
        self.__mongodb_user: str = self.__get_env("MONGODB_USER")
        self.__mongodb_password: str = self.__get_env("MONGODB_PASSWORD")
        self.__mongodb_host: str = self.__get_env("MONGODB_HOST")
        self.__youtube_url_pattern: str = self.__get_env("YOUTUBE_URL_PATTERN")

    @property
    def holodule_url(self) -> str:
        """
        ホロジュールのURLを取得する
        
        Returns:
            str: ホロジュールのURL
        """
        return self.__holodule_url

    @property
    def api_key(self) -> str:
        """
        Youtube Data API v3 のAPIキーを取得する

        Returns:
            str: APIキー
        """
        return self.__api_key

    @property
    def api_service_name(self) -> str:
        """
        Youtube Data API v3 のAPIサービス名を取得する

        Returns:
            str: APIサービス名
        """
        return self.__api_service_name

    @property
    def api_version(self) -> str:
        """
        Youtube Data API v3 のAPIバージョンを取得する

        Returns:
            str: APIバージョン
        """
        return self.__api_version

    @property
    def mongodb_user(self) -> str:
        """
        MongoDBのユーザーを取得する

        Returns:
            str: MongoDBのユーザー
        """
        return self.__mongodb_user

    @property
    def mongodb_password(self) -> str:
        """
        MongoDBのパスワードを取得する

        Returns:
            str: MongoDBのパスワード
        """
        return self.__mongodb_password

    @property
    def mongodb_host(self) -> str:
        """
        MongoDBのホスト:ポートを取得する

        Returns:
            str: MongoDBのホスト:ポート
        """
        return self.__mongodb_host

    @property
    def youtube_url_pattern(self) -> str:
        """
        Youtube URL として判定するパターンを取得する

        Returns:
            str: Youtube URL として判定するパターン
        """
        return self.__youtube_url_pattern

    def __load_env(self) -> None:
        """
        .envファイルを読み込む
        
        Raises:
            ValueError: .envファイルの読み込みに失敗した場合
        """
        try:
            load_dotenv(self.env_path)
        except Exception as e:
            raise ValueError(f"Failed to load .env file: {e}")

    def __get_env(self, key: str) -> str:
        """
        環境変数を取得する

        Args:
            key (str): 環境変数のキー
        
        Returns:
            str: 環境変数の値
        
        Raises:
            ValueError: 環境変数が設定されていない場合
        """
        value = os.environ.get(key)
        if value is None:
            raise ValueError(f"Missing environment variable: {key}")
        return value

    async def __check_url(self, url: str) -> bool:
        """
        指定したURLにアクセスできるかをチェックする

        Args:
            url (str): URL
        
        Returns:
            bool: アクセスできる場合はTrue、できない場合はFalse
        
        Raises:
            ValueError: URLが指定されていない場合
        """
        try:
            async with urllib.request.urlopen(url) as response:
                return True
        except Exception:
            return False

    async def check_holodule_url(self) -> bool:
        """
        ホロジュールのURLにアクセスできるかをチェックする

        Returns:
            bool: アクセスできる場合はTrue、できない場合はFalse
        """
        return await self.__check_url(self.__holodule_url)
