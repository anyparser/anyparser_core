from enum import Enum
from typing import Final, List

FALLBACK_API_URL: Final[str] = "https://anyparserapi.com"

# Supported OCR preset modes
OCR_PRESETS: Final[List[str]] = [
    "document",
    "handwriting",
    "scan",
    "receipt",
    "magazine",
    "invoice",
    "business-card",
    "passport",
    "driver-license",
    "identity-card",
    "license-plate",
    "medical-report",
    "bank-statement",
]


class OcrPreset(Enum):
    """Enumeration of supported OCR presets for document processing."""

    DOCUMENT = "document"
    HANDWRITING = "handwriting"
    SCAN = "scan"
    RECEIPT = "receipt"
    MAGAZINE = "magazine"
    INVOICE = "invoice"
    BUSINESS_CARD = "business-card"
    PASSPORT = "passport"
    DRIVER_LICENSE = "driver-license"
    IDENTITY_CARD = "identity-card"
    LICENSE_PLATE = "license-plate"
    MEDICAL_REPORT = "medical-report"
    BANK_STATEMENT = "bank-statement"


# Supported OCR language codes
OCR_LANGUAGES: Final[List[str]] = [
    "afr",
    "amh",
    "ara",
    "asm",
    "aze",
    "aze_cyrl",
    "bel",
    "ben",
    "bod",
    "bos",
    "bre",
    "bul",
    "cat",
    "ceb",
    "ces",
    "chi_sim",
    "chi_sim_vert",
    "chi_tra",
    "chi_tra_vert",
    "chr",
    "cos",
    "cym",
    "dan",
    "dan_frak",
    "deu",
    "deu_frak",
    "deu_latf",
    "div",
    "dzo",
    "ell",
    "eng",
    "enm",
    "epo",
    "equ",
    "est",
    "eus",
    "fao",
    "fas",
    "fil",
    "fin",
    "fra",
    "frm",
    "fry",
    "gla",
    "gle",
    "glg",
    "grc",
    "guj",
    "hat",
    "heb",
    "hin",
    "hrv",
    "hun",
    "hye",
    "iku",
    "ind",
    "isl",
    "ita",
    "ita_old",
    "jav",
    "jpn",
    "jpn_vert",
    "kan",
    "kat",
    "kat_old",
    "kaz",
    "khm",
    "kir",
    "kmr",
    "kor",
    "kor_vert",
    "lao",
    "lat",
    "lav",
    "lit",
    "ltz",
    "mal",
    "mar",
    "mkd",
    "mlt",
    "mon",
    "mri",
    "msa",
    "mya",
    "nep",
    "nld",
    "nor",
    "oci",
    "ori",
    "osd",
    "pan",
    "pol",
    "por",
    "pus",
    "que",
    "ron",
    "rus",
    "san",
    "sin",
    "slk",
    "slk_frak",
    "slv",
    "snd",
    "spa",
    "spa_old",
    "sqi",
    "srp",
    "srp_latn",
    "sun",
    "swa",
    "swe",
    "syr",
    "tam",
    "tat",
    "tel",
    "tgk",
    "tgl",
    "tha",
    "tir",
    "ton",
    "tur",
    "uig",
    "ukr",
    "urd",
    "uzb",
    "uzb_cyrl",
    "vie",
    "yid",
    "yor",
]


class OcrLanguage(Enum):
    """Enumeration of supported OCR languages for text recognition."""

    AFRIKAANS = "afr"
    AMHARIC = "amh"
    ARABIC = "ara"
    ASSAMESE = "asm"
    AZERBAIJANI = "aze"
    AZERBAIJANI_CYRILLIC = "aze_cyrl"
    BELARUSIAN = "bel"
    BENGALI = "ben"
    TIBETAN = "bod"
    BOSNIAN = "bos"
    BRETON = "bre"
    BULGARIAN = "bul"
    CATALAN = "cat"
    CEBUANO = "ceb"
    CZECH = "ces"
    SIMPLIFIED_CHINESE = "chi_sim"
    SIMPLIFIED_CHINESE_VERTICAL = "chi_sim_vert"
    TRADITIONAL_CHINESE = "chi_tra"
    TRADITIONAL_CHINESE_VERTICAL = "chi_tra_vert"
    CHEROKEE = "chr"
    CORSICAN = "cos"
    WELSH = "cym"
    DANISH = "dan"
    DANISH_FRAKTUR = "dan_frak"
    GERMAN = "deu"
    GERMAN_FRAKTUR = "deu_frak"
    GERMAN_LATIN = "deu_latf"
    DIVESH = "div"
    DZONGKHA = "dzo"
    GREEK = "ell"
    ENGLISH = "eng"
    MIDDLE_ENGLISH = "enm"
    ESPERANTO = "epo"
    EQUATORIAL_GUINEAN = "equ"
    ESTONIAN = "est"
    BASQUE = "eus"
    FAROESE = "fao"
    PERSIAN = "fas"
    FILIPINO = "fil"
    FINNISH = "fin"
    FRENCH = "fra"
    OLD_FRENCH = "frm"
    FRISIAN = "fry"
    SCOTTISH_GAELIC = "gla"
    IRISH = "gle"
    GALICIAN = "glg"
    ANCIENT_GREEK = "grc"
    GUJARATI = "guj"
    HAITIAN_CREOLE = "hat"
    HEBREW = "heb"
    HINDI = "hin"
    CROATIAN = "hrv"
    HUNGARIAN = "hun"
    ARMENIAN = "hye"
    IGBO = "iku"
    INDONESIAN = "ind"
    ICELANDIC = "isl"
    ITALIAN = "ita"
    OLD_ITALIAN = "ita_old"
    JAVANESE = "jav"
    JAPANESE = "jpn"
    JAPANESE_VERTICAL = "jpn_vert"
    KANNADA = "kan"
    GEORGIAN = "kat"
    OLD_GEORGIAN = "kat_old"
    KAZAKH = "kaz"
    KHMER = "khm"
    KIRGHIZ = "kir"
    KURDISH = "kmr"
    KOREAN = "kor"
    KOREAN_VERTICAL = "kor_vert"
    LAO = "lao"
    LATIN = "lat"
    LATVIAN = "lav"
    LITHUANIAN = "lit"
    LUXEMBOURGISH = "ltz"
    MALAYALAM = "mal"
    MARATHI = "mar"
    MACEDONIAN = "mkd"
    MALTESE = "mlt"
    MONGOLIAN = "mon"
    MAORI = "mri"
    MALAY = "msa"
    MYANMAR = "mya"
    NEPALI = "nep"
    DUTCH = "nld"
    NORWEGIAN = "nor"
    OCCITAN = "oci"
    ODISHA = "ori"
    OSD = "osd"
    PUNJABI = "pan"
    POLISH = "pol"
    PORTUGUESE = "por"
    PASHTO = "pus"
    QUECHUA = "que"
    ROMANIAN = "ron"
    RUSSIAN = "rus"
    SANSKRIT = "san"
    SINHALA = "sin"
    SLOVAK = "slk"
    SLOVAK_FRAKTUR = "slk_frak"
    SLOVENIAN = "slv"
    SINDHI = "snd"
    SPANISH = "spa"
    OLD_SPANISH = "spa_old"
    ALBANIAN = "sqi"
    SERBIAN = "srp"
    SERBIAN_LATIN = "srp_latn"
    SUNDIANESE = "sun"
    SWAHILI = "swa"
    SWEDISH = "swe"
    SYRIAC = "syr"
    TAMIL = "tam"
    TATAR = "tat"
    TELUGU = "tel"
    TAJIK = "tgk"
    TAGALOG = "tgl"
    THAI = "tha"
    TIGRINYA = "tir"
    TONGAN = "ton"
    TURKISH = "tur"
    UIGHUR = "uig"
    UKRAINIAN = "ukr"
    URDU = "urd"
    UZBEK = "uzb"
    UZBEK_CYRILLIC = "uzb_cyrl"
    VIETNAMESE = "vie"
    YIDDISH = "yid"
    YORUBA = "yor"
