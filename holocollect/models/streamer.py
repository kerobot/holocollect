from logging import getLogger

class Streamer:
    """
    ホロライブの配信者を表すクラス
    """
    def __init__(self, code: str, name: str, group: str, affiliations: list[str], 
                 image_name: str, channel_id: str, is_retired: bool = False) -> None:
        """
        Streamerクラスのインスタンスを生成する
        
        Args:
            code (str): 配信者のコード
            name (str): 配信者の名前
            group (str): 所属グループ
            affiliations (list[str]): 所属グループの配列
            image_name (str): 配信者の画像ファイル名
            channel_id (str): 配信者のチャンネルID
            is_retired (bool, optional): 引退済みかどうか. Defaults to False.
        """
        self._logger = getLogger(__name__)

        self.__code: str = code
        self.__name: str = name
        self.__group: str = group
        self.__affiliations: list[str] = affiliations
        self.__image_name: str = image_name
        self.__channel_id: str = channel_id
        self.__is_retired: bool = is_retired

    @property
    def code(self) -> str:
        """
        配信者のコードを返す
        
        Returns:
            str: 配信者のコード
        """
        return self.__code
    
    @property
    def name(self) -> str:
        """
        配信者の名前を返す
        
        Returns:
            str: 配信者の名前
        """
        return self.__name
    
    @property
    def group(self) -> str:
        """
        所属グループを返す
        
        Returns:
            str: 所属グループ
        """
        return self.__group
    
    @property
    def affiliations(self) -> list[str]:
        """
        所属グループの配列を返す
        
        Returns:
            list[str]: 所属グループの配列
        """
        return self.__affiliations
    
    @property
    def image_name(self) -> str:
        """
        配信者の画像ファイル名を返す
        
        Returns:
            str: 配信者の画像ファイル名
        """
        return self.__image_name
    
    @property
    def channel_id(self) -> str:
        """
        配信者のチャンネルIDを返す
        
        Returns:
            str: 配信者のチャンネルID
        """
        return self.__channel_id
    
    @property
    def is_retired(self) -> bool:
        """
        引退済みかどうかを返す
        
        Returns:
            bool: 引退済みかどうか
        """
        return self.__is_retired

    def to_dict(self) -> dict[str, str]:
        """
        Streamerオブジェクトを辞書形式で返す
        
        Returns:
            dict[str, str]: Streamerオブジェクトの辞書形式
        """
        data: dict[str, str] = {
            'code': str(self.code),
            'name': str(self.name),
            'group': str(self.group),
            'affiliations': str(self.affiliations),
            'image_name': str(self.image_name),
            'channel_id': str(self.channel_id),
            'is_retired': str(self.is_retired)
        }
        return data
    
    @classmethod
    def from_dict(cls, data: dict[str, str]) -> 'Streamer':
        """
        辞書形式からStreamerオブジェクトを生成する（クラスメソッド）
        
        Args:
            data (dict[str, str]): Streamerオブジェクトの辞書形式
        
        Returns:
            Streamer: Streamerオブジェクト
        """
        code = data['code']
        name = data['name']
        group = data['group']
        affiliations = eval(data['affiliations'])
        image_name = data['image_name']
        channel_id = data['channel_id']
        is_retired = eval(data['is_retired'])
        return cls(code, name, group, affiliations, image_name, channel_id, is_retired)
