from al_quran_bot.quran_client import QuranClient


def normalize_image_url(image_url: str | None) -> str | None:
    if not image_url:
        return None
    if image_url.startswith("//"):
        return "https:" + image_url
    return image_url


def build_random_verse_payload(client: QuranClient) -> tuple[str, str | None]:
    data = client.get_random_verse()
    verse = data.get("verse", {})

    translations = verse.get("translations", [])
    translation_text = translations[0].get("text") if translations else None

    verse_text = verse.get("text_imlaei")
    verse_key = verse.get("verse_key") or "noma'lum"
    image_url = normalize_image_url(verse.get("image_url"))

    lines = [
        verse_text or "[matn topilmadi]",
        translation_text or "[tarjima topilmadi]",
    ]

    caption = "\n\n".join(lines)

    surah = getSurahName(int(verse_key.split(":")[0]))
    ayah = verse_key.split(":")[1]

    caption += (
        f"\n\n{surah} surasi {ayah}-oyat Shayx Muhammad Sodiq Muhammad Yusuf tarjimasi"
    )
    return caption, image_url


def getSurahName(surah_number: int) -> str:
    surah_names = {
        1: "Fotiha",
        2: "Baqara",
        3: "Oli Imron",
        4: "Niso",
        5: "Moida",
        6: "Anʼom",
        7: "Aʼrof",
        8: "Anfol",
        9: "Tavba",
        10: "Yunus",
        11: "Hud",
        12: "Yusuf",
        13: "Raʼd",
        14: "Ibrohim",
        15: "Hijr",
        16: "Nahl",
        17: "Isro",
        18: "Kahf",
        19: "Maryam",
        20: "Toha",
        21: "Anbiyo",
        22: "Haj",
        23: "Moʼminun",
        24: "Nur",
        25: "Furqon",
        26: "Shuaro",
        27: "Naml",
        28: "Qasas",
        29: "Ankabut",
        30: "Rum",
        31: "Luqmon",
        32: "Sajda",
        33: "Ahzob",
        34: "Saba",
        35: "Fotir",
        36: "Yosin",
        37: "Soffat",
        38: "Sod",
        39: "Zumar",
        40: "Gʻofir",
        41: "Fussilat",
        42: "Shoʻro",
        43: "Zuhruf",
        44: "Duxon",
        45: "Joshiya",
        46: "Ahqof",
        47: "Muhammad",
        48: "Fath",
        49: "Hujurot",
        50: "Qof",
        51: "Zoriyot",
        52: "Tur",
        53: "Najm",
        54: "Qamar",
        55: "Rahmon",
        56: "Voʼqea",
        57: "Hadid",
        58: "Mujodala",
        59: "Hashr",
        60: "Mumtahana",
        61: "Soff",
        62: "Juma",
        63: "Munofiqun",
        64: "Tagʻobun",
        65: "Taloq",
        66: "Tahrim",
        67: "Mulk",
        68: "Qalam",
        69: "Hoqo",
        70: "Maʼorij",
        71: "Nuh",
        72: "Jin",
        73: "Muzzammil",
        74: "Muddassir",
        75: "Qiyomat",
        76: "Inson",
        77: "Mursalot",
        78: "Nabaʼ",
        79: "Noziʼot",
        80: "Abasa",
        81: "Takvir",
        82: "Infitor",
        83: "Mutoffifin",
        84: "Inshiqoq",
        85: "Buruj",
        86: "Toriq",
        87: "Aʼlo",
        88: "Gʻoshiya",
        89: "Fajr",
        90: "Balad",
        91: "Shams",
        92: "Layl",
        93: "Zuho",
        94: "Sharh",
        95: "Tiyn",
        96: "Alaq",
        97: "Qadr",
        98: "Bayyina",
        99: "Zalzala",
        100: "Odiyot",
        101: "Qoriʼa",
        102: "Takosur",
        103: "Asr",
        104: "Humaza",
        105: "Fil",
        106: "Quraysh",
        107: "Moʼun",
        108: "Kavsar",
        109: "Kofirun",
        110: "Nasr",
        111: "Masad",
        112: "Ixlos",
        113: "Falaq",
        114: "Nos",
    }
    return surah_names.get(surah_number, "Nomaʼlum sura")
