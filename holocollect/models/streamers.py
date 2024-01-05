import pymongo
from logging import getLogger
from holocollect.models.streamer import StreamerModel
from holocollect.mongodb import MongoDB

class StreamerCollection():
    """
    StreamerModelオブジェクトのコレクションクラス
    """
    def __init__(self):
        """
        StreamerCollectionクラスのコンストラクタ
        """
        self._logger = getLogger(__name__)
        self.streamers: dict[str, StreamerModel] = {
            "ホロライブ" : StreamerModel(code="HL0000", name="ホロライブ", group="hololive", affiliations=["bland","jp"], image_name="hololive.jpg", channel_id="@hololive"),

            "ときのそら" : StreamerModel(code="HL0001", name="ときのそら", group="hololive", affiliations=["gen0","jp"], image_name="tokino_sora.jpg", channel_id="@TokinoSora"),
            "ロボ子さん" : StreamerModel(code="HL0002", name="ロボ子さん", group="hololive", affiliations=["gen0","jp"], image_name="robokosan.jpg", channel_id="@Robocosan"),
            "さくらみこ" : StreamerModel(code="HL0003", name="さくらみこ", group="hololive", affiliations=["gen0","jp"], image_name="sakura_miko.jpg", channel_id="@SakuraMiko"),
            "星街すいせい" : StreamerModel(code="HL0004", name="星街すいせい", group="hololive", affiliations=["gen0","jp"], image_name="hoshimachi_suisei.jpg", channel_id="@HoshimachiSuisei"),
            "AZKi" : StreamerModel(code="HL0005", name="AZKi", group="hololive", affiliations=["gen0","jp"], image_name="azki.jpg", channel_id="@AZKi"),

            "夜空メル" : StreamerModel(code="HL0101", name="夜空メル", group="hololive", affiliations=["gen1","jp"], image_name="yozora_mel.jpg", channel_id="@YozoraMel"),
            "アキ・ローゼンタール" : StreamerModel(code="HL0102", name="アキ・ローゼンタール", group="hololive", affiliations=["gen1","jp"], image_name="aki_rosenthal.jpg", channel_id="@AkiRosenthal"),
            "赤井はあと" : StreamerModel(code="HL0103", name="赤井はあと", group="hololive", affiliations=["gen1","jp"], image_name="haachama.jpg", channel_id="@AkaiHaato"),
            "白上フブキ" : StreamerModel(code="HL0104", name="白上フブキ", group="hololive", affiliations=["gen1","gamers","jp"], image_name="shirakami_fubuki.jpg", channel_id="@ShirakamiFubuki"),
            "夏色まつり" : StreamerModel(code="HL0105", name="夏色まつり", group="hololive", affiliations=["gen1","jp"], image_name="natsuiro_matsuri.jpg", channel_id="@NatsuiroMatsuri"),

            "湊あくあ" : StreamerModel(code="HL0201", name="湊あくあ", group="hololive", affiliations=["gen2","jp"], image_name="minato_aqua.jpg", channel_id="@MinatoAqua"),
            "紫咲シオン" : StreamerModel(code="HL0202", name="紫咲シオン", group="hololive", affiliations=["gen2","jp"], image_name="murasaki_shion.jpg", channel_id="@MurasakiShion"),
            "百鬼あやめ" : StreamerModel(code="HL0203", name="百鬼あやめ", group="hololive", affiliations=["gen2","jp"], image_name="nakiri_ayame.jpg", channel_id="@NakiriAyame"),
            "癒月ちょこ" : StreamerModel(code="HL0204", name="癒月ちょこ", group="hololive", affiliations=["gen2","jp"], image_name="yuzuki_choco.jpg", channel_id="@YuzukiChoco"),
            "大空スバル" : StreamerModel(code="HL0205", name="大空スバル", group="hololive", affiliations=["gen2","jp"], image_name="oozora_subaru.jpg", channel_id="@OozoraSubaru"),

            "大神ミオ" : StreamerModel(code="HL0G02", name="大神ミオ", group="hololive", affiliations=["gamers","jp"], image_name="ookami_mio.jpg", channel_id="@OokamiMio"),
            "猫又おかゆ" : StreamerModel(code="HL0G03", name="猫又おかゆ", group="hololive", affiliations=["gamers","jp"], image_name="nekomata_okayu.jpg", channel_id="@NekomataOkayu"),
            "戌神ころね" : StreamerModel(code="HL0G04", name="戌神ころね", group="hololive", affiliations=["gamers","jp"], image_name="inugami_korone.jpg", channel_id="@InugamiKorone"),

            "兎田ぺこら" : StreamerModel(code="HL0301", name="兎田ぺこら", group="hololive", affiliations=["gen3","jp"], image_name="usada_pekora.jpg", channel_id="@usadapekora"),
            "潤羽るしあ" : StreamerModel(code="HL0302", name="潤羽るしあ", group="hololive", affiliations=["gen3","jp"], image_name="uruha_rushia.jpg", channel_id="@hololive", is_retired=True),
            "不知火フレア" : StreamerModel(code="HL0303", name="不知火フレア", group="hololive", affiliations=["gen3","jp"], image_name="shiranui_flare.jpg", channel_id="@ShiranuiFlare"),
            "白銀ノエル" : StreamerModel(code="HL0304", name="白銀ノエル", group="hololive", affiliations=["gen3","jp"], image_name="shirogane_noel.jpg", channel_id="@ShiroganeNoel"),
            "宝鐘マリン" : StreamerModel(code="HL0305", name="宝鐘マリン", group="hololive", affiliations=["gen3","jp"], image_name="housyou_marine.jpg", channel_id="@HoushouMarine"),

            "天音かなた" : StreamerModel(code="HL0401", name="天音かなた", group="hololive", affiliations=["gen4","jp"], image_name="amane_kanata.jpg", channel_id="@AmaneKanata"),
            "桐生ココ" : StreamerModel(code="HL0402", name="桐生ココ", group="hololive", affiliations=["gen4","jp"], image_name="kiryu_coco.jpg", channel_id="@KiryuCoco", is_retired=True),
            "角巻わため" : StreamerModel(code="HL0403", name="角巻わため", group="hololive", affiliations=["gen4","jp"], image_name="tsunomaki_watame.jpg", channel_id="@TsunomakiWatame"),
            "常闇トワ" : StreamerModel(code="HL0404", name="常闇トワ", group="hololive", affiliations=["gen4","jp"], image_name="tokoyami_towa.jpg", channel_id="@TokoyamiTowa"),
            "姫森ルーナ" : StreamerModel(code="HL0405", name="姫森ルーナ", group="hololive", affiliations=["gen4","jp"], image_name="himemori_luna.jpg", channel_id="@HimemoriLuna"),

            "獅白ぼたん" : StreamerModel(code="HL0501", name="獅白ぼたん", group="hololive", affiliations=["gen5","jp"], image_name="shishiro_botan.jpg", channel_id="@ShishiroBotan"),
            "雪花ラミィ" : StreamerModel(code="HL0502", name="雪花ラミィ", group="hololive", affiliations=["gen5","jp"], image_name="yukihana_lamy.jpg", channel_id="@YukihanaLamy"),
            "尾丸ポルカ" : StreamerModel(code="HL0503", name="尾丸ポルカ", group="hololive", affiliations=["gen5","jp"], image_name="omaru_polka.jpg", channel_id="@OmaruPolka"),
            "桃鈴ねね" : StreamerModel(code="HL0504", name="桃鈴ねね", group="hololive", affiliations=["gen5","jp"], image_name="momosuzu_nene.jpg", channel_id="@MomosuzuNene"),
            "魔乃アロエ" : StreamerModel(code="HL0505", name="魔乃アロエ", group="hololive", affiliations=["gen5","jp"], image_name="mano_aloe.jpg", channel_id="@hololive", is_retired=True),

            "ラプラス" : StreamerModel(code="HL0601", name="ラプラス・ダークネス", group="hololive", affiliations=["gen6","jp"], image_name="laplus_darknesss.jpg", channel_id="@LaplusDarknesss"),
            "鷹嶺ルイ" : StreamerModel(code="HL0602", name="鷹嶺ルイ", group="hololive", affiliations=["gen6","jp"], image_name="takane_lui.jpg", channel_id="@TakaneLui"),
            "博衣こより" : StreamerModel(code="HL0603", name="博衣こより", group="hololive", affiliations=["gen6","jp"], image_name="hakui_koyori.jpg", channel_id="@HakuiKoyori"),
            "沙花叉クロヱ" : StreamerModel(code="HL0604", name="沙花叉クロヱ", group="hololive", affiliations=["gen6","jp"], image_name="sakamata_chloe.jpg", channel_id="@SakamataChloe"),
            "風真いろは" : StreamerModel(code="HL0605", name="風真いろは", group="hololive", affiliations=["gen6","jp"], image_name="kazama_iroha.jpg", channel_id="@kazamairoha"),

            "hololive DEV_IS" : StreamerModel(code="HLDI00", name="hololive DEV_IS", group="hololive_DEV_IS)", affiliations=["bland","jp"], image_name="hololive_dev_is.jpg", channel_id="@hololiveDEV_IS"),
            "火威青" : StreamerModel(code="HLDI01", name="火威青", group="hololive_DEV_IS", affiliations=["dev_is","jp"], image_name="hiodoshi_ao.jpg", channel_id="@HiodoshiAo"),
            "儒烏風亭らでん" : StreamerModel(code="HLDI02", name="儒烏風亭らでん", group="hololive_DEV_IS", affiliations=["dev_is","jp"], image_name="juufuutei_raden.jpg", channel_id="@JuufuuteiRaden"),
            "一条莉々華" : StreamerModel(code="HLDI03", name="一条莉々華", group="hololive_DEV_IS", affiliations=["dev_is","jp"], image_name="otonose_kanade.jpg", channel_id="@OtonoseKanade"),
            "音乃瀬奏" : StreamerModel(code="HLDI04", name="音乃瀬奏", group="hololive_DEV_IS", affiliations=["dev_is","jp"], image_name="ichijou_ririka.jpg", channel_id="@IchijouRirika"),
            "轟はじめ" : StreamerModel(code="HLDI05", name="轟はじめ", group="hololive_DEV_IS", affiliations=["dev_is","jp"], image_name="todoroki_hajime.jpg", channel_id="@TodorokiHajime"),

            "Risu" : StreamerModel(code="HLID01", name="Ayunda Risu", group="hololive_id", affiliations=["gen1","id"], image_name="ayunda_risu.jpg", channel_id="@AyundaRisu"),
            "Moona" : StreamerModel(code="HLID02", name="Moona Hoshinova", group="hololive_id",affiliations=["gen1","id"], image_name="moona_hoshinova.jpg", channel_id="@MoonaHoshinova"),
            "Iofi" : StreamerModel(code="HLID03", name="Airani Iofifteen", group="hololive_id", affiliations=["gen1","id"], image_name="airani_iofifteen.jpg", channel_id="@AiraniIofifteen"),

            "Ollie" : StreamerModel(code="HLID04", name="Kureiji Ollie", group="hololive_id", affiliations=["gen2","id"], image_name="kureiji_ollie.jpg", channel_id="@KureijiOllie"),
            "Anya" : StreamerModel(code="HLID05", name="Anya Melfissa", group="hololive_id", affiliations=["gen2","id"], image_name="anya_melfissa.jpg", channel_id="@AnyaMelfissa"),
            "Reine" : StreamerModel(code="HLID06", name="Pavolia Reine", group="hololive_id", affiliations=["gen2","id"], image_name="pavolia_reine.jpg", channel_id="@PavoliaReine"),

            "Zeta" : StreamerModel(code="HLID07", name="Vestia Zeta", group="hololive_id", affiliations=["gen3","id"], image_name="vestia_zeta.jpg", channel_id="@VestiaZeta"),
            "Kaela" : StreamerModel(code="HLID08", name="Kaela Kovalskia",group="hololive_id", affiliations=["gen3","id"], image_name="kaela_kovalskia.jpg", channel_id="@KaelaKovalskia"),
            "Kobo" : StreamerModel(code="HLID09", name="Kobo Kanaeru", group="hololive_id", affiliations=["gen3","id"], image_name="kobo_kanaeru.jpg", channel_id="@KoboKanaeru"),

            "Calli" : StreamerModel(code="HLEN01", name="Mori Calliope", group="hololive_en", affiliations=["gen1","en"], image_name="mori_calliope.jpg", channel_id="@MoriCalliope"),
            "Kiara" : StreamerModel(code="HLEN02", name="Takanashi Kiara", group="hololive_en", affiliations=["gen1","en"], image_name="takanashi_kiara.jpg", channel_id="@TakanashiKiara"),
            "Ina" : StreamerModel(code="HLEN03", name="Ninomae Ina'nis", group="hololive_en", affiliations=["gen1","en"], image_name="ninomae_ina'nis.jpg", channel_id="@NinomaeInanis"),
            "Gura" : StreamerModel(code="HLEN04", name="Gawr Gura", group="hololive_en", affiliations=["gen1","en"], image_name="gawr_gura.jpg", channel_id="@GawrGura"),
            "Amelia" : StreamerModel(code="HLEN05", name="Watson Amelia", group="hololive_en", affiliations=["gen1","en"], image_name="watson_amelia.jpg", channel_id="@WatsonAmelia"),

            "IRyS" : StreamerModel(code="HLEN06", name="IRyS", group="hololive_en", affiliations=["hope","gen2","en"], image_name="irys.jpg", channel_id="@IRyS"),

            "Fauna" : StreamerModel(code="HLEN07", name="Ceres Fauna", group="hololive_en", affiliations=["gen2","en"], image_name="ceres_fauna.jpg", channel_id="@CeresFauna"),
            "Kronii" : StreamerModel(code="HLEN08", name="Ouro Kronii", group="hololive_en", affiliations=["gen2","en"], image_name="ouro_kronii.jpg", channel_id="@OuroKronii"),
            "Mumei" : StreamerModel(code="HLEN09", name="Nanashi Mumei", group="hololive_en", affiliations=["gen2","en"], image_name="nanashi_mumei.jpg", channel_id="@NanashiMumei"),
            "Baelz" : StreamerModel(code="HLEN10", name="Hakos Baelz", group="hololive_en", affiliations=["gen2","en"], image_name="hakos_baelz.jpg", channel_id="@HakosBaelz"),
            "Sana" : StreamerModel(code="HLEN11", name="Tsukumo Sana", group="hololive_en", affiliations=["gen2","en"], image_name="tsukumo_sana.jpg", channel_id="@TsukumoSana", is_retired=True),

            "Shiori" : StreamerModel(code="HLEN12", name="Shiori Novella", group="hololive_en", affiliations=["gen3","en"], image_name="shiori_novella.jpg", channel_id="@ShioriNovella"),
            "Bijou" : StreamerModel(code="HLEN13", name="Koseki Bijou", group="hololive_en", affiliations=["gen3","en"],image_name="koseki_bijou.jpg", channel_id="@KosekiBijou"),
            "Nerissa" : StreamerModel(code="HLEN14", name="Nerissa Ravencroft", group="hololive_en", affiliations=["gen3","en"], image_name="nerissa_ravencroft.jpg", channel_id="@NerissaRavencroft"),
            "FUWAMOCO" : StreamerModel(code="HLEN15", name="FUWAMOCO", group="hololive_en", affiliations=["gen3","en"], image_name="fuwamoco.jpg", channel_id="@FUWAMOCOch"),
        }

    def get_streamer_by_name(self, name: str) -> StreamerModel | None:
        """
        指定した名前（短縮名）のStreamerModelオブジェクトを取得する関数
        
        Args:
            name (str): 配信者の名前（短縮名）
        
        Returns:
            StreamerModel | None: 指定した名前（短縮名）のStreamerModelオブジェクト
        """
        return self.streamers.get(name, None)

    def save_to_mongodb(self) -> None:
        """
        StreamerModelオブジェクトをMongoDBに保存する関数
        """
        try:
            db = MongoDB.getInstance().holoduledb
            collection = db.streamers
            for streamer in self.streamers.values():
                # codeをキーにして更新
                query = {"code": streamer.code}
                dump = streamer.model_dump(by_alias=True, exclude=["id"])
                collection.replace_one(query, dump, upsert=True)
        except pymongo.errors.ConnectionError as e:
            self._logger.error("MongoDB 接続に失敗しました。%s", e, exc_info=True)
            raise
        except pymongo.errors.OperationFailure as e:
            self._logger.error("MongoDB 操作に失敗しました。%s", e, exc_info=True)
            raise
        except pymongo.errors.PyMongoError as e:
            self._logger.error("MongoDB エラーが発生しました。%s", e, exc_info=True)
            raise
