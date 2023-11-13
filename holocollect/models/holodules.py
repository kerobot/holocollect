import csv
import pymongo
from logging import getLogger
from holocollect.models.holodule import Holodule

class Holodules:
    """
    Holoduleオブジェクトのコレクションクラス
    """
    def __init__(self, holodules: list[Holodule] = []) -> None:
        """
        Holodulesクラスのインスタンスを生成する

        Args:
            holodules (list[Holodule], optional): Holoduleオブジェクトのリスト. Defaults to [].
        """
        self._logger = getLogger(__name__)

        self.holodules: list[Holodule] = holodules
        self.index: int = 0

    def __iter__(self) -> 'Holodules':
        """
        イテレータを返す

        Returns:
            Holodules: Holodulesオブジェクト
        """
        self.index = 0
        return self

    def __next__(self) -> Holodule:
        """
        次のHoloduleオブジェクトを返す

        Returns:
            Holodule: Holoduleオブジェクト
        """
        if self.index < len(self.holodules):
            result = self.holodules[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration

    def __len__(self) -> int:
        """
        Holoduleオブジェクトの数を返す
        
        Returns:
            int: Holoduleオブジェクトの数
        """
        return len(self.holodules)

    def __getitem__(self, index: int) -> Holodule:
        """
        指定したインデックスのHoloduleオブジェクトを返す

        Args:
            index (int): インデックス
        """
        return self.holodules[index]

    def append(self, holodule: Holodule) -> None:
        """
        Holoduleオブジェクトを追加する
        
        Args:
            holodule (Holodule): Holoduleオブジェクト
        """
        self.holodules.append(holodule)

    def remove_at(self, index: int) -> None:
        """
        指定したインデックスのHoloduleオブジェクトを削除する
        
        Args:
            index (int): インデックス
        """
        self.holodules.pop(index)

    def output_to_csv(self, filepath: str) -> None:
        """
        CSVファイルに出力する
        
        Args:
            filepath (str): CSVファイルのパス
        """
        try:
            with open(filepath, "w", newline="", encoding="utf_8_sig") as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=",")
                csvwriter.writerow([attr for attr in vars(Holodule())])
                for holodule in self.holodules:
                    csvwriter.writerow([value for value in vars(holodule).values()])
        except (FileNotFoundError, PermissionError) as e:
            self._logger.error("CSV エラーが発生しました。%s", e, exc_info=True)
            raise

    def save_to_mongodb(self, uri: str, db_name: str, collection_name: str) -> None:
        """
        MongoDBに保存する
        
        Args:
            uri (str): MongoDBのURI
            db_name (str): データベース名
            collection_name (str): コレクション名
        """
        try:
            client = pymongo.MongoClient(uri)
            db = client[db_name]
            collection = db[collection_name]
            video_ids = [holodule.video_id for holodule in self.holodules]
            collection.delete_many({"video_id": {"$in": video_ids}})
            docs = [holodule.to_dict() for holodule in self.holodules]
            collection.insert_many(docs)
        except pymongo.errors.ConnectionError as e:
            self._logger.error("MongoDB 接続に失敗しました。%s", e, exc_info=True)
            raise
        except pymongo.errors.OperationFailure as e:
            self._logger.error("MongoDB 操作に失敗しました。%s", e, exc_info=True)
            raise
        except pymongo.errors.PyMongoError as e:
            self._logger.error("MongoDB エラーが発生しました。%s", e, exc_info=True)
            raise
        finally:
            client.close()
