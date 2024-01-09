from pydantic import BaseModel
import pymongo
import csv
from logging import getLogger
from app.models.schedule import ScheduleModel
from app.mongodb import MongoDB

logger = getLogger(__name__)

class ScheduleCollection(BaseModel):
    """
    ScheduleModelオブジェクトのコレクションクラス
    """
    schedules: list[ScheduleModel] = []
    index: int = 0

    def __iter__(self) -> 'ScheduleCollection':
        """
        イテレータを返す

        Returns:
            ScheduleCollection: ScheduleCollectionオブジェクト
        """
        self.index = 0
        return self

    def __next__(self) -> ScheduleModel:
        """
        次のScheduleModelオブジェクトを返す

        Returns:
            ScheduleModel: ScheduleModelオブジェクト
        """
        if self.index < len(self.schedules):
            result = self.schedules[self.index]
            self.index += 1
            return result
        else:
            raise StopIteration

    def __len__(self) -> int:
        """
        ScheduleModelオブジェクトの数を返す
        
        Returns:
            int: ScheduleModelオブジェクトの数
        """
        return len(self.schedules)

    def __getitem__(self, index: int) -> ScheduleModel:
        """
        指定したインデックスのScheduleModelオブジェクトを返す

        Args:
            index (int): インデックス
        """
        return self.schedules[index]

    def append(self, schedule: ScheduleModel) -> None:
        """
        ScheduleModelオブジェクトを追加する
        
        Args:
            schedule (ScheduleModel): ScheduleModelオブジェクト
        """
        self.schedules.append(schedule)

    def remove_at(self, index: int) -> None:
        """
        指定したインデックスのScheduleModelオブジェクトを削除する
        
        Args:
            index (int): インデックス
        """
        self.schedules.pop(index)

    def output_to_csv(self, filepath: str) -> None:
        """
        ScheduleModelオブジェクトをCSVファイルに出力する関数
        
        Args:
            filepath (str): CSVファイルのパス
        """
        try:
            with open(filepath, "w", newline="", encoding="utf_8_sig") as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=",")
                csvwriter.writerow([attr for attr in vars(ScheduleModel())])
                for schedule in self.schedules:
                    csvwriter.writerow([value for value in vars(schedule).values()])
        except (FileNotFoundError, PermissionError) as e:
            self._logger.error("CSV エラーが発生しました。%s", e, exc_info=True)
            raise

    def save_to_mongodb(self) -> None:
        """
        ScheduleModelオブジェクトをMongoDBに保存する関数
        """
        try:
            db = MongoDB.getInstance().holoduledb
            collection = db.schedules
            # video_id が一致するドキュメントを削除
            video_ids = [schedule.video_id for schedule in self.schedules]
            collection.delete_many({"video_id": {"$in": video_ids}})
            # ScheduleModelオブジェクトをドキュメントに変換して一括登録
            dumps = [schedule.model_dump(by_alias=True, exclude=["id"]) for schedule in self.schedules]
            collection.insert_many(dumps)
        except pymongo.errors.ConnectionError as e:
            self.logger.error("MongoDB 接続に失敗しました。%s", e, exc_info=True)
            raise
        except pymongo.errors.OperationFailure as e:
            self.logger.error("MongoDB 操作に失敗しました。%s", e, exc_info=True)
            raise
        except pymongo.errors.PyMongoError as e:
            self.logger.error("MongoDB エラーが発生しました。%s", e, exc_info=True)
            raise
