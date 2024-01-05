import re
from datetime import datetime, timezone, timedelta, date
from logging import getLogger
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from holocollect.settings import get_youtube_settings, get_holodule_settings
from holocollect.models.schedule import ScheduleModel
from holocollect.models.schedules import ScheduleCollection
from holocollect.models.streamers import StreamerCollection

holodule_settings = get_holodule_settings()
youtube_settings = get_youtube_settings()

class Collector:
    """
    【ホロライブ】ホロジュールと Youtube の動画情報を取得して MongoDB へ登録するクラス
    """

    def __init__(self):
        """
        Collectorクラスのコンストラク
        """
        # Logger 関連
        self._logger = getLogger(__name__)
        # WebDriver 関連
        self.__driver = None
        self.__wait = None
        # Model 関連
        self.__streamers = StreamerCollection()
        self.__schedules = ScheduleCollection()
        # YouTube Data API v3 を利用するための準備
        self.__youtube = build(youtube_settings.api_service_name, youtube_settings.api_version, developerKey=youtube_settings.api_key, cache_discovery=False)

    def __setup_options(self) -> webdriver.ChromeOptions:
        """
        Selenium オプションをセットアップする関数
        
        Returns:
            webdriver.ChromeOptions: オプション
        """
        options = webdriver.ChromeOptions()
        # ヘッドレスモードとする
        options.add_argument('--headless=new')
        return options

    def __get_schedules(self) -> ScheduleCollection:
        """
        ホロジュール情報を取得する関数
        
        Returns:
            ScheduleCollection: ホロジュール情報のコレクション
        """
        # 取得対象の URL に遷移
        self.__driver.get(holodule_settings.url)
        # <div class="holodule" style="margin-top:10px;">が表示されるまで待機する
        self.__wait.until(EC.presence_of_element_located((By.CLASS_NAME, "holodule")))
        # ページソースの取得
        html = self.__driver.page_source.encode("utf-8")
        # ページソースの解析（パーサとして lxml を指定）
        soup = BeautifulSoup(html, "lxml")
        # タイトルの取得（確認用）
        head = soup.find("head")
        title = head.find("title").text
        self._logger.info('TITLE : %s', title)

        # TODO : ここからはページの構成に合わせて決め打ち = ページの構成が変わったら動かない
        # スケジュールの取得
        schedules = ScheduleCollection()
        date_string = ""
        today = date.today()
        tab_pane = soup.find("div", class_="tab-pane show active")
        containers = tab_pane.find_all("div", class_="container")

        for container in containers:
            # 日付のみ取得
            div_date = container.find("div", class_="holodule navbar-text")
            if div_date is not None:
                date_text = div_date.text.strip()
                match_date = re.search(r"[0-9]{1,2}/[0-9]{1,2}", date_text)
                dates = match_date.group(0).split("/")
                month = int(dates[0])
                day = int(dates[1])
                year = today.year
                if month == 12 and today.month == 1:
                    year = year - 1
                elif month == 1 and today.month == 12:
                    year = year + 1
                date_string = f"{year}/{month}/{day}"

            # 配信者毎のスケジュール
            thumbnails = container.find_all("a", class_="thumbnail")
            if thumbnails is not None:
                for thumbnail in thumbnails:
                    # Youtube URL
                    stream_url = thumbnail.get("href")
                    if stream_url is None or re.match(youtube_settings.url_pattern, stream_url) is None:
                        continue
                    # 時刻（先に取得しておいた日付と合体）
                    div_time = thumbnail.find("div", class_="col-4 col-sm-4 col-md-4 text-left datetime")
                    if div_time is None:
                        continue
                    time_text = div_time.text.strip()
                    match_time = re.search(r"[0-9]{1,2}:[0-9]{1,2}", time_text)
                    times = match_time.group(0).split(":")
                    hour = int(times[0])
                    minute = int(times[1])
                    datetime_string = f"{date_string} {hour}:{minute}"
                    stream_datetime = datetime.strptime(datetime_string, "%Y/%m/%d %H:%M")
                    # 配信者の名前
                    div_name = thumbnail.find("div", class_="col text-right name")
                    if div_name is None:
                        continue
                    stream_name = div_name.text.strip()
                    # リストに追加
                    streamer = self.__streamers.get_streamer_by_name(stream_name)
                    if streamer is None:
                        continue
                    schedule = ScheduleModel(code=streamer.code, url=stream_url, streaming_at=stream_datetime, name=stream_name)
                    schedules.append(schedule)
        return schedules

    def __get_youtube_video_info(self, youtube_url: str) -> tuple:
        """
        Youtube 動画情報を取得する関数
        
        Args:
            youtube_url (str): Youtube の URL
        
        Returns:
            tuple: 動画情報（video_id, title, description, published_at, channel_id, channel_title, tags）
        
        Raises:
            HttpError: Youtube の API でエラーが発生した場合
            Exception: その他のエラーが発生した場合
        """
        try:
            self._logger.info('YOUTUBE_URL : %s', youtube_url)
            # Youtube の URL から ID を取得
            match_video = re.search(r"^[^v]+v=(.{11}).*", youtube_url)
            if not match_video:
                self._logger.error("YouTube URL が不正です。")
                return None
            video_id = match_video.group(1)

            # Youtube はスクレイピングを禁止しているので YouTube Data API (v3) で情報を取得
            search_response = self.__youtube.videos().list(
                # 結果として snippet のみを取得
                part="snippet",
                # 検索条件は id
                id=video_id,
                # 1件のみ取得
                maxResults=1
            ).execute()

            # 検索結果から情報を取得
            for search_result in search_response.get("items", []):
                # id
                video_id = search_result["id"]
                # タイトル
                title = search_result["snippet"]["title"]
                # 説明
                description = search_result["snippet"]["description"]
                # 投稿日
                datetime_string = search_result["snippet"]["publishedAt"]
                published_at = datetime.fromisoformat(datetime_string).astimezone(tz=timezone(timedelta(hours=+9)))
                # チャンネルID
                channel_id = search_result["snippet"]["channelId"]
                # チャンネルタイトル
                channel_title = search_result["snippet"]["channelTitle"]
                # タグ（設定されていない＝キーが存在しない場合あり）
                tags = search_result["snippet"].setdefault("tags", [])
                # 取得した情報を返却
                return (video_id, title, description, published_at, channel_id, channel_title, tags)

            self._logger.error("指定したIDに一致する動画がありません。")
            return None

        except HttpError as e:
            self._logger.error("HTTP エラー %d が発生しました。%s" % (e.resp.status, e.content))
            raise
        except Exception as e:
            self._logger.error("エラーが発生しました。%s" % e)
            raise

    def get_holodules(self) -> ScheduleCollection:
        """
        ホロジュールのスクレイピングと Youtube 動画情報から、ホロジュール情報のコレクションを取得する関数
        
        Returns:
            ScheduleCollection: ホロジュール情報のコレクション
        
        Raises:
            Exception: ホロジュールの取得に失敗した場合
        """
        try:
            # オプションのセットアップ
            options = self.__setup_options()
            # ドライバの初期化（オプション（ヘッドレスモード）とプロファイルを指定）
            self.__driver = webdriver.Chrome(options=options)
            # 指定したドライバに対して最大で10秒間待つように設定する
            self.__wait = WebDriverWait(self.__driver, 10)
            # ホロジュール情報の取得
            self.__schedules = self.__get_schedules()
            # Youtube情報の取得
            for schedule in self.__schedules:
                try:
                    # ホロジュール情報に動画情報を付与
                    self._logger.info('SCHEDULE_NAME : %s', schedule.name)
                    self._logger.info('SCHEDULE_AT : %s', schedule.streaming_at)
                    video_info = self.__get_youtube_video_info(schedule.url)
                    if video_info == None:
                        continue
                    schedule.set_video_info(*video_info)
                    self._logger.info('SCHEDULE_TITLE : %s', schedule.title)
                except Exception as e:
                    self._logger.error("エラーが発生しました。", exc_info=True)
                    raise e
        except Exception as e:
            self._logger.error("エラーが発生しました。", exc_info=True)
            raise e
        finally:
            # ドライバを閉じる
            if self.__driver is not None and len(self.__driver.window_handles) > 0:
                self.__driver.close()
        return self.__schedules

    def save_to_mongodb(self):
        """
        配信者情報とホロジュール情報を MongoDB へ登録する関数
        
        Raises:
            Exception: MongoDB への登録に失敗した場合
        """
        # 配信者情報の登録
        self.__streamers.save_to_mongodb()
        # ホロジュール情報の登録
        self.__schedules.save_to_mongodb()

    # CSV への出力
    def output_to_csv(self, filepath: str):
        """
        ホロジュール情報を CSV へ出力する関数
        
        Args:
            filepath (str): 出力するCSVファイルのパス
        
        Raises:
            Exception: CSV への出力に失敗した場合
        """
        # ホロジュール情報の出力
        self.__schedules.output_to_csv(filepath)
