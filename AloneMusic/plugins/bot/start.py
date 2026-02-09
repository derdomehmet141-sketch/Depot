import random
import time

from py_yt import VideosSearch
from pyrogram import filters
from pyrogram.enums import ChatType
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, CallbackQuery

import config
from AloneMusic import app
from AloneMusic.misc import _boot_
from AloneMusic.plugins.sudo.sudoers import sudoers_list
from AloneMusic.utils.database import (add_served_chat, add_served_user,
                                       blacklisted_chats, get_lang,
                                       is_banned_user, is_on_off)
from AloneMusic.utils.decorators.language import LanguageStart
from AloneMusic.utils.formatters import get_readable_time
from AloneMusic.utils.inline import help_pannel, private_panel, start_panel
from config import BANNED_USERS
from strings import get_string

# --- CALLBACK HANDLER (Geri ve Kapat Tuşu İçin) ---
@app.on_callback_query(filters.regex(pattern=r"^(settingsback_helper|close)$"))
async def control_cb(client, query: CallbackQuery):
    callback_data = query.data.strip()
    language = await get_lang(query.message.chat.id)
    _ = get_string(language)

    if callback_data == "close":
        await query.message.delete()
        await query.answer("Menü Kapatıldı", show_alert=False)
    
    elif callback_data == "settingsback_helper":
        # Geri tuşuna basıldığında ana paneli tekrar yükler
        buttons = private_panel(_)
        # Kapat butonunu geri dönülen menüye de ekleyelim
        buttons.append([InlineKeyboardButton(text="🗑 Kapat", callback_data="close")])
        
        await query.edit_message_text(
            text=_["start_2"].format(query.from_user.mention, app.mention),
            reply_markup=InlineKeyboardMarkup(buttons),
        )

# --- START KOMUTLARI ---

@app.on_message(filters.command(["start"]) & filters.private & ~BANNED_USERS)
@LanguageStart
async def start_pm(client, message: Message, _):
    await add_served_user(message.from_user.id)
    await message.react("🍓")
    
    if len(message.text.split()) > 1:
        name = message.text.split(None, 1)[1]
        
        if name[0:4] == "help":
            keyboard = help_pannel(_)
            # Yardım paneline kapat butonu ekle
            keyboard.append([InlineKeyboardButton(text="🗑 Kapat", callback_data="close")])
            return await message.reply_text(
                text=_["help_1"].format(config.SUPPORT_CHAT),
                reply_markup=InlineKeyboardMarkup(keyboard),
            )
            
        if name[0:3] == "sud":
            await sudoers_list(client=client, message=message, _=_)
            return

        if name[0:3] == "inf":
            m = await message.reply_text("🔎")
            query = (str(name)).replace("info_", "", 1)
            query = f"https://www.youtube.com/watch?v={query}"
            results = VideosSearch(query, limit=1)
            for result in (await results.next())["result"]:
                title = result["title"]
                duration = result["duration"]
                views = result["viewCount"]["short"]
                channellink = result["channel"]["link"]
                channel = result["channel"]["name"]
                link = result["link"]
                published = result["publishedTime"]
                
            searched_text = _["start_6"].format(
                title, duration, views, published, channellink, channel, app.mention
            )
            key = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(text=_["S_B_8"], url=link),
                        InlineKeyboardButton(text=_["S_B_9"], url=config.SUPPORT_CHAT),
                    ],
                    [InlineKeyboardButton(text="🗑 Kapat", callback_data="close")]
                ]
            )
            await m.delete()
            return await message.reply_text(
                text=searched_text,
                reply_markup=key,
            )
    else:
        out = private_panel(_)
        # Ana menüye Kapat butonu ekle
        out.append([InlineKeyboardButton(text="🗑 Kapat", callback_data="close")])
        await message.reply_text(
            text=_["start_2"].format(message.from_user.mention, app.mention),
            reply_markup=InlineKeyboardMarkup(out),
        )

@app.on_message(filters.command(["start"]) & filters.group & ~BANNED_USERS)
@LanguageStart
async def start_gp(client, message: Message, _):
    out = start_panel(_)
    # Grup paneline kapat butonu ekle
    out.append([InlineKeyboardButton(text="🗑 Kapat", callback_data="close")])
    uptime = int(time.time() - _boot_)
    await message.reply_text(
        text=_["start_1"].format(app.mention, get_readable_time(uptime)),
        reply_markup=InlineKeyboardMarkup(out),
    )
    return await add_served_chat(message.chat.id)

@app.on_message(filters.new_chat_members, group=-1)
async def welcome(client, message: Message):
    for member in message.new_chat_members:
        try:
            language = await get_lang(message.chat.id)
            _ = get_string(language)
            
            if await is_banned_user(member.id):
                try:
                    await message.chat.ban_member(member.id)
                except:
                    pass
            
            if member.id == app.id:
                if message.chat.type != ChatType.SUPERGROUP:
                    await message.reply_text(_["start_4"])
                    return await app.leave_chat(message.chat.id)
                
                if message.chat.id in await blacklisted_chats():
                    await message.reply_text(_["start_5"].format(app.mention, f"https://t.me/{app.username}?start=sudolist", config.SUPPORT_CHAT))
                    return await app.leave_chat(message.chat.id)

                out = start_panel(_)
                out.append([InlineKeyboardButton(text="🗑 Kapat", callback_data="close")])
                await message.reply_text(
                    text=_["start_3"].format(
                        message.from_user.first_name if message.from_user else "User",
                        app.mention, message.chat.title, app.mention
                    ),
                    reply_markup=InlineKeyboardMarkup(out),
                )
                await add_served_chat(message.chat.id)
        except Exception as ex:
            print(ex)
