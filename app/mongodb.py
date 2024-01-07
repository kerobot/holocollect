import atexit
from pymongo import MongoClient
from app.settings import get_mongo_settings

mongo_settings = get_mongo_settings()

class MongoDB:
    """
    MongoDBの接続を管理するシングルトンクラス
    """
    _instance = None

    @staticmethod
    def getInstance() -> MongoClient:
        """
        MongoDBクラスのインスタンスを取得する関数
        
        Returns:
            MongoClient: MongoClientのインスタンス
        """
        if MongoDB._instance is None:
            MongoDB()
        return MongoDB._instance

    def __init__(self):
        """
        MongoDBクラスのコンストラクタ（DB接続）
        """
        if MongoDB._instance is not None:
            raise Exception("このクラスはシングルトンです。")
        else:
            MongoDB._instance = MongoClient(mongo_settings.uri)
            # クリーンアップ関数の登録
            atexit.register(self.close)

    def close(self):
        """
        MongoDBクラスのデストラクタ（DB切断）
        """
        if MongoDB._instance is not None:
            MongoDB._instance.close()
