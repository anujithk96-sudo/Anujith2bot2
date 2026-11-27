import re
import asyncio
from collections import defaultdict
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode

# ==========================================
# BOT SETTINGS
# ==========================================

CHANNELS = [-1003911112940]
AUTH_CHANNEL = -1003926879089
BOT_USERNAME = "Anujith2bot"
BANNER_PHOTO = "https://ibb.co/cS5zrTGD"


# ==========================================
# SERIAL MAPPING
# ==========================================

SERIALS_MAPPING = {
    "kanmashi": "Kanmashi",
    "karnan": "Karnan",
    "valyettan": "Valyettan",
    "pranayavilasam": "Pranayavilasam",
    "durga": "Durga",
    "chembarathy": "Chembarathy",
    "saregamapa": "SaReGaMaPa",
    "saregamapa_lil_champs": "SaReGaMaPa Lil Champs",
    "kudumbasametham": "Kudumbasametham",
    "meghasandhesham": "Meghasandhesham",
    "seethayanam": "Seethayanam",
    "krishnagadha": "Krishnagadha",
    "meghasandesam": "Meghasandesam",
    "aval_arundhati": "Aval Arundhati",
    "akale": "Akale",
    "snehapoorvam_shyama": "Snehapoorvam Shyama",
    "mangalyam": "Mangalyam",
    "manathe_kottaram": "Manathe Kottaram",
    "ashwathi_nakshatram": "Ashwathi Nakshatram",
    "kudumbashree_sharada": "Kudumbashree Sharada",
    "bigg_boss": "Bigg Boss",
    "taste_time": "Taste Time",
    "sindhu_bhairavi": "Sindhu Bhairavi",
    "comedy_cooks": "Comedy Cooks",
    "ivar_vivahitharayal": "Ivar Vivahitharayal",
    "oru_kochu_swapnam": "Oru Kochu Swapnam",
    "advocate_anjali": "Advocate Anjali",
    "kattathe_kilikoodu": "Kattathe Kilikoodu",
    "ee_puzhayum_kadannu": "Ee Puzhayum Kadannu",
    "sindoorapottu": "Sindoorapottu",
    "star_singer": "Star Singer",
    "teacheramma": "Teacheramma",
    "mazha_thorum_munpe": "Mazha Thorum Munpe",
    "pavithram": "Pavithram",
    "ishtam_mathram": "Ishtam Mathram",
    "santhwanam": "Santhwanam 2",
    "snehakkoottu": "Snehakkoottu",
    "mounaragam": "Mounaragam",
    "patharamattu": "Patharamattu",
    "amma_manassu": "Amma Manassu",
    "chempaneer_poovu": "Chempaneer Poovu",
    "dharmma_yoddhavu_garudan": "Dharmma Yoddhavu Garudan",
    "othiri_othiri_swapnangal": "Othiri Othiri Swapnangal",
    "ottashikharam": "Ottashikharam",
    "archana_chechi_llb": "Archana Chechi LLB",
    "super_kanmani": "Super Kanmani",
    "marimayam": "Marimayam",
    "oru_chiri_iru_chiri_bumper_chiri":
        "Oru Chiri Iru Chiri Bumper Chiri",
    "the_great_family_challenge": "The Great Family Challenge",
    "roopavathi": "Roopavathi",
    "thenmavin_kombath": "Thenmavin Kombath",
    "punnaram": "Punnaram",
    "anju_sundarikal": "Anju Sundarikal",
    "amme_mookambike": "Amme Mookambike",
    "peythozhiyathe": "Peythozhiyathe",
    "chattambipparu": "Chattambipparu",
    "hridayam": "Hridayam",
    "kanyadaanam": "Kanyadaanam",
    "swayamavarapanthal": "Swayamavarapanthal",
    "mangalyam_thanthunanena": "Mangalyam Thanthunanena",
    "mukhachithram": "Mukhachithram",
    "kunjumalakha": "Kunjumalakha",
    "cheffum_kuttyolum": "Cheffum Kuttyolum",
    "sabaritheertham": "Sabaritheertham",
}


# ==========================================
# VIDEO QUALITY PATTERN
# ==========================================

QUALITY_PATTERN = r"(?<!\d)(\d{3,4})\s*[pP](?!\w)"


# ==========================================
# GET ORIGINAL FILE NAME
# ==========================================

def get_file_name(message):
    if message.document:
        return message.document.file_name or "Media File"

    if message.video:
        return message.video.file_name or "Media File"

    return "Media File"


# ==========================================
# FIND SERIAL NAME
# ==========================================

def find_serial_name(filename):
    normalized = re.sub(r"[._-]+", " ", filename.lower())
    normalized = re.sub(r"\s+", " ", normalized).strip()

    mapping_items = sorted(
        SERIALS_MAPPING.items(),
        key=lambda item: len(item[0]),
        reverse=True
    )

    for key, display_name in mapping_items:
        search_name = key.replace("_", " ").lower()

        pattern = (
            r"(?<!\w)"
            + re.escape(search_name)
            + r"(?!\w)"
        )

        if re.search(pattern, normalized):
            return display_name

    return clean_unknown_name(filename)


# ==========================================
# CLEAN UNKNOWN SERIAL NAME
# ==========================================

def clean_unknown_name(filename):
    name = re.sub(
        r"\.(mkv|mp4|avi|mov|webm|m4v|mpeg|mpg)$",
        "",
        filename,
        flags=re.IGNORECASE
    )

    name = re.sub(
        r"\bS\d+[ ._-]*E(?:P(?:ISODE)?)?[ ._-]*\d+"
        r"(?:[ ._-]*-[ ._-]*E?\d+)?",
        "",
        name,
        flags=re.IGNORECASE
    )

    name = re.sub(
        r"\bSeason[ ._-]*\d+\b",
        "",
        name,
        flags=re.IGNORECASE
    )

    name = re.sub(
        r"\bEpisode[ ._-]*\d+(?:[ ._-]*-[ ._-]*\d+)?",
        "",
        name,
        flags=re.IGNORECASE
    )

    name = re.sub(
        QUALITY_PATTERN,
        "",
        name,
        flags=re.IGNORECASE
    )

    name = re.sub(
        r"\b(HS|WEB|WEB-DL|HDRIP|HDTV|X264|X265)\b",
        "",
        name,
        flags=re.IGNORECASE
    )

    name = re.sub(r"[._]+", " ", name)
    name = re.sub(r"\s+", " ", name)

    return name.strip(" -_.") or "Malayalam Serial"


# ==========================================
# GET SEASON
# ==========================================

def get_season(filename):

    match = re.search(
        r"(?<![A-Za-z0-9])S(\d+)\s*E\d+",
        filename,
        re.IGNORECASE
    )

    if match:
        return match.group(1).zfill(2)

    match = re.search(
        r"\bSeason[ ._-]*(\d+)\b",
        filename,
        re.IGNORECASE
    )

    if match:
        return match.group(1).zfill(2)

    match = re.search(
        r"(?<![A-Za-z0-9])S(\d{1,2})(?![A-Za-z0-9])",
        filename,
        re.IGNORECASE
    )

    if match:
        return match.group(1).zfill(2)

    return "01"


# ==========================================
# GET VIDEO QUALITY FROM FILENAME ONLY
# ==========================================

def get_quality(filename, message=None):
    """Return quality from Telegram's actual video dimensions.

    Filename tags are deliberately not trusted: a file named 1080p may
    contain a 720p video. If Telegram supplies no dimensions, report
    Unknown instead of displaying a guessed quality.
    """
    width = height = None

    if message is not None:
        media = getattr(message, "video", None)
        if media is not None:
            width = getattr(media, "width", None)
            height = getattr(media, "height", None)

        # Videos sent as documents expose dimensions through
        # DocumentAttributeVideo.
        if not height:
            document = getattr(message, "document", None)
            for attribute in getattr(document, "attributes", []) or []:
                attr_height = getattr(attribute, "height", None)
                attr_width = getattr(attribute, "width", None)
                if attr_height and attr_width:
                    width, height = attr_width, attr_height
                    break

    if not height:
        return "Unknown"

    standard_qualities = (144, 240, 360, 480, 576, 720, 1080, 1440, 2160)
    nearest = min(standard_qualities, key=lambda value: abs(value - height))
    if abs(nearest - height) <= 8:
        return f"{nearest}p"

    return f"{height}p"



# ==========================================
# GET CLEAN SERIAL NAME
# ==========================================

def get_clean_serial_name(filename):
    return find_serial_name(filename)


# ==========================================
# GET FILE LINK
# SERIAL NAME ONLY
# ==========================================

def make_start_link(serial_name):

    slug = re.sub(
        r"[^A-Za-z0-9]+",
        "-",
        serial_name
    ).strip("-")

    payload = f"getfile-{slug}"

    return (
        f"https://telegram.me/{BOT_USERNAME}"
        f"?start={payload}"
    )


# ==========================================
# SMART BATCH PROCESSING STORAGE
# SERIAL + SEASON + QUALITY WISE
# ==========================================

pending_batches = defaultdict(list)
batch_timers = {}
BATCH_WAIT_SECONDS = 7


# ==========================================
# EXTRACT EPISODE NUMBERS
# Supports S01E1086, S01E1086-1087,
# EP1086, Episode 1086 and 1086-1087
# ==========================================

def extract_episode_numbers(filename):
    episodes = set()

    patterns = (
        r"(?<![A-Za-z0-9])S\d{1,2}[ ._-]*E(?:P)?[ ._-]*(\d{1,4})"
        r"(?:[ ._-]*-[ ._-]*(?:E(?:P)?[ ._-]*)?(\d{1,4}))?(?!\d)",
        r"(?<![A-Za-z0-9])(?:EPISODE|EP|E)[ ._-]*(\d{1,4})"
        r"(?:[ ._-]*-[ ._-]*(?:(?:EPISODE|EP|E)[ ._-]*)?(\d{1,4}))?(?!\d)",
        r"(?<!\d)(\d{3,4})[ ._-]+-[ ._-]*(\d{3,4})(?!\d)",
    )

    for pattern in patterns:
        for match in re.finditer(pattern, filename, re.IGNORECASE):
            for value in match.groups():
                if value:
                    number = int(value)
                    if number > 0:
                        episodes.add(number)

    return episodes


# ==========================================
# FORMAT EPISODE NUMBERS
# ==========================================

def format_episode_range(episodes):
    episodes = sorted(set(episodes))

    if not episodes:
        return "N/A"
    if len(episodes) == 1:
        return str(episodes[0])

    continuous = all(
        episodes[index + 1] == episodes[index] + 1
        for index in range(len(episodes) - 1)
    )

    if continuous:
        return f"{episodes[0]}-{episodes[-1]}"

    # Do not claim a continuous range when episode numbers are missing.
    return ", ".join(str(number) for number in episodes)


# ==========================================
# PROCESS ONE SERIAL/SEASON/QUALITY BATCH
# ==========================================

async def process_batch(client, batch_key):
    try:
        # Debounce: wait until this serial's files stop arriving.
        await asyncio.sleep(BATCH_WAIT_SECONDS)

        if not pending_batches.get(batch_key):
            return

        batch_items = pending_batches.pop(batch_key, [])
        current_task = asyncio.current_task()
        if batch_timers.get(batch_key) is current_task:
            batch_timers.pop(batch_key, None)

        chat_id, serial_name, season, quality = batch_key
        all_episodes = set()

        for item in batch_items:
            all_episodes.update(
                extract_episode_numbers(get_file_name(item))
            )

        episode = format_episode_range(all_episodes)

        caption = (
            "<b>🍁Anujith Allu TV Serials🍁</b>\n\n"
            f"📁 <b>File Name :</b> {serial_name}\n"
            f"🎞️ <b>Season :</b> {season}\n"
            f"📌 <b>Episode :</b> {episode}\n"
            f"🎬 <b>Quality :</b> {quality}"
        )

        buttons = InlineKeyboardMarkup([[
            InlineKeyboardButton(
                "📥 Get File",
                url=make_start_link(serial_name)
            )
        ]])

        await client.send_photo(
            chat_id=AUTH_CHANNEL,
            photo=BANNER_PHOTO,
            caption=caption,
            parse_mode=ParseMode.HTML,
            reply_markup=buttons
        )

        print(
            "Auto-post successful | "
            f"Name: {serial_name} | Season: {season} | "
            f"Episode: {episode} | Quality: {quality} | "
            f"Files: {len(batch_items)}"
        )

    except asyncio.CancelledError:
        # A new matching file arrived; its handler will schedule a fresh timer.
        return
    except Exception as error:
        print(f"Auto-Formatter Error: {error}")


# ==========================================
# AUTO POST HANDLER
# MULTI-SERIAL + SEASON + QUALITY SUPPORT
# ==========================================

@Client.on_message(
    filters.chat(CHANNELS)
    & (filters.document | filters.video)
)
async def auto_post_formatter(client, message):
    filename = get_file_name(message)
    serial_name = get_clean_serial_name(filename)
    season = get_season(filename)
    quality = get_quality(filename, message)

    # Separate groups prevent different serials, seasons or qualities
    # from being combined into one channel post.
    batch_key = (
        message.chat.id,
        serial_name,
        season,
        quality
    )

    pending_batches[batch_key].append(message)

    # Restart only this batch's timer when another matching file arrives.
    old_task = batch_timers.get(batch_key)
    if old_task and not old_task.done():
        old_task.cancel()

    batch_timers[batch_key] = asyncio.create_task(
        process_batch(client, batch_key)
    )

    print(
        f"Batch received | {serial_name} | Season {season} | "
        f"Quality {quality} | Files: {len(pending_batches[batch_key])}"
    )
