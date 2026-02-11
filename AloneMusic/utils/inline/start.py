from pyrogram.types import InlineKeyboardButton

import config
from AloneMusic import app


def start_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_1"], url=f"https://t.me/{app.username}?startgroup=true"
            ),
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT),
        ],
    ]
    return buttons


def private_panel(_):
    # Hata koruması: OWNER_ID liste ise ilkini al, değilse direkt kullan
    owner_id = (
        config.OWNER_ID[0] if isinstance(config.OWNER_ID, list) else config.OWNER_ID
    )

    buttons = [
        [
            # Gruba Ekle Butonu
            InlineKeyboardButton(
                text=_["S_B_3"],
                url=f"https://t.me/{app.username}?startgroup=true",
            )
        ],
        [
            # Destek Grubu Butonu
            InlineKeyboardButton(text=_["S_B_2"], url=config.SUPPORT_CHAT),
            # Sahip Butonu
            InlineKeyboardButton(text="𝐒ᴀʜіʙі ˼", user_id=owner_id),
        ],
        [
            # Yardım/Menü Butonu (Geri işlevi için)
            InlineKeyboardButton(text=_["S_B_4"], callback_data="settings_back_helper")
        ],
    ]
    return buttons
