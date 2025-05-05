import re
from datetime import datetime, timezone, timedelta
from typing_extensions import Annotated
from pydantic import BaseModel, ConfigDict, Field, computed_field
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]
UTC = timezone.utc
JST = timezone(timedelta(hours=+9), "JST")


class ScheduleModel(BaseModel):
    """
    スケジュール情報を管理するクラス

    Args:
        _id (PyObjectId, optional): スケジュールID
        code (str, optional): 配信者コード
        video_id (str, optional): 動画ID
        streaming_at (datetime, optional): 配信日時
        name (str, optional): 配信者名
        title (str, optional): タイトル
        url (str, optional): Youtube URL
        description (str, optional): 概要
        published_at (datetime, optional): 投稿日時
        channel_id (str, optional): チャンネルID
        channel_title (str, optional): チャンネル名
        tags (list[str], optional): タグ
        model_config (ConfigDict): モデルの設定辞書
    """

    id: PyObjectId | None = Field(
        alias="_id", default=None, description="スケジュールID"
    )
    code: str | None = Field(default=None, description="配信者コード")
    video_id: str | None = Field(default=None, description="動画ID")
    streaming_at: datetime | None = Field(
        default_factory=lambda: datetime.now(tz=JST), description="配信日時"
    )
    name: str | None = Field(default=None, description="配信者名")
    title: str | None = Field(default=None, description="タイトル")
    url: str | None = Field(default=None, description="Youtube URL")
    description: str | None = Field(default=None, description="概要")
    published_at: datetime | None = Field(
        default_factory=lambda: datetime.now(tz=JST), description="投稿日時"
    )
    channel_id: str | None = Field(default=None, description="チャンネルID")
    channel_title: str | None = Field(default=None, description="チャンネル名")
    tags: list[str] = Field(default_factory=list, description="タグ")

    model_config = ConfigDict(
        populate_by_name=True,  # エイリアス名でのアクセスを許可するか（例えば id と _id）
        arbitrary_types_allowed=True,  # 任意の型を許可するか
        json_schema_extra={
            "example": {
                "code": "HL0000",
                "video_id": "動画ID",
                "streaming_at": "2023-12-01T12:00:00Z",
                "name": "配信者名",
                "title": "タイトル",
                "url": "Youtube URL",
                "description": "概要",
                "published_at": "2023-12-01T12:00:00Z",
                "channel_id": "チャンネルID",
                "channel_title": "チャンネル名",
                "tags": [],
            }
        },
    )

    @property
    @computed_field
    def key(self) -> str:
        """
        スケジュールのキーを返す

        Returns:
            str: スケジュールのキー
        """
        return (
            self.code + "_" + self.streaming_at.strftime("%Y%m%d_%H%M%S")
            if (self.code is not None and self.streaming_at is not None)
            else ""
        )

    def set_video_info(
        self,
        video_id: str,
        title: str,
        description: str,
        published_at: datetime,
        channel_id: str,
        channel_title: str,
        tags: list[str],
    ):
        """
        Youtubeの動画情報を設定する関数

        Args:
            video_id (str): 動画ID
            title (str): 動画タイトル
            description (str): 動画説明文
            published_at (datetime): 動画公開日時
            channel_id (str): チャンネルID
            channel_title (str): チャンネルタイトル
            tags (List[str]): タグ
        """
        self.video_id = video_id
        self.title = title
        self.description = re.sub(r"[\r\n\"\']", "", description)[:1000]
        self.published_at = published_at
        self.channel_id = channel_id
        self.channel_title = channel_title
        self.tags = tags
