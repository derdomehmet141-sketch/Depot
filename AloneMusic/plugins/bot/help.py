from typing import Union

from pyrogram import filters, types
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from AloneMusic import app
from AloneMusic.utils import help_pannel
from AloneMusic.utils.database import get_lang
from AloneMusic.utils.decorators.language import LanguageStart, languageCB
from AloneMusic.utils.inline.help import private_help_panel
from config import BANNED_USERS, SUPPORT_CHAT
from strings import get_string, helpers


### 1. YARDIM MENÜSÜ (Özel Mesaj ve Geri Dönüş)
@app.on_message(filters.command(["help"]) & filters.private & ~BANNED_USERS)
@app.on_callback_query(filters.regex("settings_back_helper") & ~BANNED_USERS)
async def helper_private(
    client: app, update: Union[types.Message, types.CallbackQuery]
):
    is_callback = isinstance(update, types.CallbackQuery)

    if is_callback:
        try:
            await update.answer()
        except:
            pass
        chat_id = update.message.chat.id
    else:
        try:
            await update.delete()
        except:
            pass
        chat_id = update.chat.id

    language = await get_lang(chat_id)
    _ = get_string(language)
    keyboard = help_pannel(_, True)

    help_text = _["help_1"].format(SUPPORT_CHAT)

    if is_callback:
        await update.edit_message_text(help_text, reply_markup=keyboard)
    else:
        await update.reply_text(help_text, reply_markup=keyboard)


### 2. GRUP İÇİ YARDIM KOMUTU
@app.on_message(filters.command(["help"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def help_com_group(client, message: Message, _):
    keyboard = private_help_panel(_)
    await message.reply_text(_["help_2"], reply_markup=InlineKeyboardMarkup(keyboard))


### 3. YARDIM DETAYLARI VE ALT BUTONLAR
@app.on_callback_query(filters.regex(r"help_callback") & ~BANNED_USERS)
@languageCB
async def helper_cb(client, callback_query: types.CallbackQuery, _):
    # Callback verisini güvenli bir şekilde alalım
    cb_data = callback_query.data.strip().split()
    if len(cb_data) < 2:
        return

    cb = cb_data[1]

    # Geri ve Kapat Butonları - Callback dataları handlerlar ile aynı olmalı
    keyboard = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text="⬅️ Geri", callback_data="settings_back_helper"
                ),
                InlineKeyboardButton(text="🗑️ Kapat", callback_data="close_menu"),
            ]
        ]
    )

    if cb == "hb1":
        await callback_query.edit_message_text(helpers.HELP_1, reply_markup=keyboard)
    elif cb == "hb2":
        await callback_query.edit_message_text(helpers.HELP_2, reply_markup=keyboard)
    elif cb == "hb3":
        await callback_query.edit_message_text(helpers.HELP_3, reply_markup=keyboard)

    await callback_query.answer()


### 4. KAPATMA BUTONU HANDLERI
@app.on_callback_query(filters.regex("close_menu") & ~BANNED_USERS)
async def close_menu_handler(client, query: types.CallbackQuery):
    try:
        await query.message.delete()
        if query.message.reply_to_message:
            await query.message.reply_to_message.delete()
    except:
        pass
    finally:
        await query.answer("Menü Kapatıldı", show_alert=False)
