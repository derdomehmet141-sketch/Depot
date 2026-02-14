#
# Copyright (C) 2021-2022 by TheAloneteam@Github, < https://github.com/TheAloneTeam >.
# All rights reserved.

from typing import Union
from pyrogram import filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from AloneMusic import app

# --- BUTONLAR VE MENÜLER ---

def help_pannel(_, START: Union[bool, int] = None):
    """
    Ana yardım paneli. 
    START True ise ayarlardan gelmiştir (Geri butonu gösterilir).
    START None/False ise direkt komutla gelmiştir (Kapat butonu gösterilir).
    """
    buttons = [
        [
            InlineKeyboardButton(text=_["H_B_1"], callback_data="help_callback hb1"),
            InlineKeyboardButton(text=_["H_B_2"], callback_data="help_callback hb2"),
        ],
    ]
    
    # Geri / Kapat mantığı
    if START:
        # Ayarlar menüsüne geri döner
        buttons.append([
            InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="settings_back_helper")
        ])
    else:
        # Menüyü tamamen kapatır
        buttons.append([
            InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")
        ])
        
    return InlineKeyboardMarkup(buttons)


def help_back_markup(_):
    """
    Alt yardım sayfalarındayken (hb1, hb2 vs.) ana yardım menüsüne dönmeyi sağlar.
    """
    return InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text=_["BACK_BUTTON"], callback_data="help_back"),
                InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")
            ]
        ]
    )


def private_help_panel(_):
    """Özel mesaj buton paneli"""
    return [
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                url=f"https://t.me/{app.username}?start=help",
            ),
        ],
    ]

# --- GERİ TUŞUNU ÇALIŞTIRAN MANTIK (HANDLER) ---
# Eğer bu kısım kodunda yoksa geri tuşu asla çalışmaz.

@app.on_callback_query(filters.regex("help_back"))
async def help_back_menu_handler(client, query: CallbackQuery):
    """
    'help_back' verisi geldiğinde ana yardım panelini tekrar yükler.
    """
    try:
        # Burada dil desteğini (get_str veya _) çağırman gerekebilir
        # Örnek olarak standart bir 'dil' değişkeni varsayıyoruz
        await query.answer("Ana menüye dönülüyor...")
        await query.edit_message_reply_markup(
            reply_markup=help_pannel(_)
        )
    except Exception as e:
        print(f"Geri dönerken hata oluştu: {e}")


@app.on_callback_query(filters.regex("close"))
async def close_menu_handler(client, query: CallbackQuery):
    """Kapat butonuna basıldığında mesajı siler."""
    await query.message.delete()
    await query.answer("Menü kapatıldı.")
