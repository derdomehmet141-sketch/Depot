from pyrogram import Client, errors
from pyrogram.enums import ChatMemberStatus, ParseMode

import config

from ..logging import LOGGER


class Alone(Client):
    def __init__(self):
        LOGGER(__name__).info("Bot Başlatılıyor...")
        super().__init__(
            name="AloneMusic",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            bot_token=config.BOT_TOKEN,
            in_memory=True,
            parse_mode=ParseMode.HTML,
            max_concurrent_transmissions=7,
        )

    async def start(self):
        await super().start()
        self.id = self.me.id
        self.name = self.me.first_name + " " + (self.me.last_name or "")
        self.username = self.me.username
        self.mention = self.me.mention

        try:
            await self.send_message(
                chat_id=config.LOGGER_ID,
                text=f"<u><b>» {self.mention} ʙᴏᴛ ʙᴀşʟᴀᴛɪʟᴅɪ :</b></u>\n\nɪᴅ : <code>{self.id}</code>\nᴀᴅ : {self.name}\nᴋᴜʟʟᴀɴɪᴄɪ ᴀᴅɪ : @{self.username}",
            )
        except (errors.ChannelInvalid, errors.PeerIdInvalid):
            LOGGER(__name__).error(
                "Bot log grubuna/kanalına erişemedi. Lütfen botu log kanalınıza eklediğinizden emin olun."
            )
            exit()
        except Exception as ex:
            LOGGER(__name__).error(
                f"Bot log grubuna/kanalına erişirken bir hata oluştu.\n Sebep : {type(ex).__name__}."
            )
            exit()

        a = await self.get_chat_member(config.LOGGER_ID, self.id)
        if a.status != ChatMemberStatus.ADMINISTRATOR:
            LOGGER(__name__).error(
                "Lütfen botu log grubunuzda/kanalınızda yönetici yapın."
            )
            exit()
        LOGGER(__name__).info(f"Müzik Botu {self.name} olarak başlatıldı.")

    async def stop(self):
        await super().stop()
