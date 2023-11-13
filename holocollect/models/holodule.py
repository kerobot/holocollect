import re
import datetime
from logging import getLogger

class Holodule:
    """
    ホロライブの配信予定を表すクラス
    """
    def __init__(self, code: str = "", url: str = "", datetime: datetime.datetime = None, name: str = ""):
        """
        Holoduleクラスのインスタンスを生成する

        Args:
            code (str, optional): 配信者のコード. Defaults to "".
            url (str, optional): 配信者のチャンネルURL. Defaults to "".
            datetime (datetime.datetime, optional): 配信日時. Defaults to None.
            name (str, optional): 配信者の名前. Defaults to "".
        """
        self._logger = getLogger(__name__)

        self.__code: str = code
        self.__url: str = url
        self.__datetime: datetime.datetime = datetime
        self.__name: str = name
        self.__video_id: str = ""
        self.__title: str = ""
        self.__description: str = ""
        self.__published_at: str = ""
        self.__channel_id: str = ""
        self.__channel_title: str = ""
        self.__tags: list[str] = []

    @property
    def key(self) -> str:
        """
        ホロジュールのキー（コード_年月日_時分秒）を返す

        Returns:
            str: ホロジュールのキー（コード_年月日_時分秒）
        """
        _code: str = self.__code;
        _dttm: str = self.__datetime.strftime("%Y%m%d_%H%M%S") if self.__datetime is not None else ""
        return _code + "_" + _dttm if ( len(_code) > 0 and len(_dttm) > 0 ) else ""

    @property
    def code(self) -> str:
        """
        配信者のコードを返す

        Returns:
            str: 配信者のコード
        """
        return self.__code
    
    @property
    def url(self) -> str:
        """
        配信者のチャンネルURLを返す

        Returns:
            str: 配信者のチャンネルURL
        """
        return self.__url
    
    @property
    def datetime(self) -> datetime.datetime:
        """
        配信日時を返す

        Returns:
            datetime.datetime: 配信日時
        """
        return self.__datetime
    
    @property
    def name(self) -> str:
        """
        配信者の名前を返す

        Returns:
            str: 配信者の名前
        """
        return self.__name
    
    @property
    def video_id(self) -> str:
        """
        動画IDを返す

        Returns:
            str: 動画ID
        """
        return self.__video_id
    
    @property
    def title(self) -> str:
        """
        動画タイトルを返す

        Returns:
            str: 動画タイトル
        """
        return self.__title
    
    @property
    def description(self) -> str:
        """
        動画説明文を返す

        Returns:
            str: 動画説明文
        """
        return self.__description
    
    @property
    def published_at(self) -> str:
        """
        動画公開日時を返す

        Returns:
            str: 動画公開日時
        """
        return self.__published_at
    
    @property
    def channel_id(self) -> str:
        """
        チャンネルIDを返す

        Returns:
            str: チャンネルID
        """
        return self.__channel_id
    
    @property
    def channel_title(self) -> str:
        """
        チャンネルタイトルを返す

        Returns:
            str: チャンネルタイトル
        """
        return self.__channel_title
    
    @property
    def tags(self) -> list[str]:
        """
        タグを返す

        Returns:
            list[str]: タグ
        """
        return self.__tags

    def set_video_info(self, video_id: str, title: str, description: str, published_at: str, 
                       channel_id: str, channel_title: str, tags: list[str]):
        """
        Youtubeの動画情報を設定する

        Args:
            video_id (str): 動画ID
            title (str): 動画タイトル
            description (str): 動画説明文
            published_at (str): 動画公開日時
            channel_id (str): チャンネルID
            channel_title (str): チャンネルタイトル
            tags (List[str]): タグ
        """
        self.__video_id = video_id
        self.__title = title
        self.__description = re.sub(r'[\r\n\"\']', '', description)[:1000]
        self.__published_at = published_at
        self.__channel_id = channel_id
        self.__channel_title = channel_title
        self.__tags = tags

    def to_dict(self) -> dict[str, str]:
        """
        Holoduleオブジェクトを辞書形式で返す

        Returns:
            dict[str, str]: Holoduleオブジェクトの辞書形式
        """
        data: dict[str, str] = {
            'key': str(self.key),
            'code': str(self.code),
            'video_id': str(self.video_id),
            'datetime': str(self.datetime.strftime("%Y%m%d %H%M%S")),
            'name': str(self.name),
            'title': str(self.title),
            'url': str(self.url),
            'description': str(self.description),
            'published_at': str(self.published_at),
            'channel_id': str(self.channel_id),
            'channel_title': str(self.channel_title),
            'tags': str(self.tags)
        }
        return data

    @classmethod
    def from_dict(cls, data: dict[str, str]) -> 'Holodule':
        """
        辞書形式からHoloduleオブジェクトを生成する（クラスメソッド）

        Args:
            data (dict[str, str]): Holoduleオブジェクトの辞書形式

        Returns:
            Holodule: Holoduleオブジェクト
        """
        code = data.get('code', '')
        url = data.get('url', '')
        datetime_str = data.get('datetime', '')
        name = data.get('name', '')
        video_id = data.get('video_id', '')
        title = data.get('title', '')
        description = data.get('description', '')
        published_at = data.get('published_at', '')
        channel_id = data.get('channel_id', '')
        channel_title = data.get('channel_title', '')
        tags = data.get('tags', '').split(',')
        tags = [tag.strip() for tag in tags if tag.strip()]

        if datetime_str:
            datetime_obj = datetime.datetime.strptime(datetime_str, '%Y%m%d %H%M%S')
        else:
            datetime_obj = None

        holodule = cls(code=code, url=url, datetime=datetime_obj, name=name)
        holodule.set_video_info(video_id, title, description, published_at, channel_id, channel_title, tags)

        return holodule
