from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from AloneMusic import app
from AloneMusic.utils.database import add_served_chat
from config import LOGGER_ID as LOG_GROUP_ID


async def yeni_mesaj(chat_id: int, mesaj: str, reply_markup=None):
    await app.send_message(chat_id=chat_id, text=mesaj, reply_markup=reply_markup)


@app.on_message(filters.new_chat_members)
async def on_new_chat_members(client: Client, message: Message):
    if app.id in [user.id for user in message.new_chat_members]:
        ekleyen = (
            message.from_user.mention if message.from_user else "Bilinmeyen Kullanıcı"
        )
        baslik = message.chat.title
        kullanici_adi = (
            f"@{message.chat.username}" if message.chat.username else "Gizli"
        )
        chat_id = message.chat.id
        uye_sayisi = await client.get_chat_members_count(chat_id)

        bildirim = (
            f"✫ <b><u>YENİ GRUP</u></b> :\n\n"
            f"SOHBET ID : {chat_id}\n"
            f"KULLANICI ADI : {kullanici_adi}\n"
            f"GRUP BAŞLIĞI : {baslik}\n"
            f"TOPLAM ÜYE : {uye_sayisi}\n\n"
            f"EKLEYEN : {ekleyen}"
        )

        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        message.from_user.first_name, user_id=message.from_user.id
                    )
                ]
            ]
        )

        await add_served_chat(chat_id)
        await yeni_mesaj(LOG_GROUP_ID, bildirim, reply_markup)


@app.on_message(filters.left_chat_member)
async def on_left_chat_member(client: Client, message: Message):
    if app.id == message.left_chat_member.id:
        cikaran = (
            message.from_user.mention if message.from_user else "Bilinmeyen Kullanıcı"
        )
        baslik = message.chat.title
        kullanici_adi = (
            f"@{message.chat.username}" if message.chat.username else "Gizli"
        )
        chat_id = message.chat.id

        ayrilis_mesaji = (
            f"✫ <b><u>GRUPTAN AYRILDI</u></b> :\n\n"
            f"SOHBET ID : {chat_id}\n"
            f"KULLANICI ADI : {kullanici_adi}\n"
            f"GRUP BAŞLIĞI : {baslik}\n\n"
            f"ÇIKARAN : {cikaran}"
        )

        reply_markup = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        message.from_user.first_name, user_id=message.from_user.id
                    )
                ]
            ]
        )
        await yeni_mesaj(LOG_GROUP_ID, ayrilis_mesaji, reply_markup)
