#
# Copyright (C) 2021-2022 by TheAloneteam@Github, < https://github.com/TheAloneTeam >.
# This file is part of < https://github.com/TheAloneTeam/AloneMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TheAloneTeam/AloneMusic/blob/master/LICENSE >
#
# All rights reserved.

from pyrogram import Client

import config

from ..logging import LOGGER

assistants = []
assistantids = []


class Userbot(Client):
    def __init__(self):
        self.one = Client(
            name="AloneMusic1",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING1),
            no_updates=True,
        )
        self.two = Client(
            name="AloneMusic2",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING2),
            no_updates=True,
        )
        self.three = Client(
            name="AloneMusic3",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING3),
            no_updates=True,
        )
        self.four = Client(
            name="AloneMusic4",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING4),
            no_updates=True,
        )
        self.five = Client(
            name="AloneMusic5",
            api_id=config.API_ID,
            api_hash=config.API_HASH,
            session_string=str(config.STRING5),
            no_updates=True,
        )

    async def start(self):
        LOGGER(__name__).info("Asistanlar Başlatılıyor...")

        if config.STRING1:
            await self.one.start()
            assistants.append(1)
            try:
                await self.one.send_message(config.LOGGER_ID, "Asistan Başlatıldı")
            except:
                LOGGER(__name__).error(
                    "Asistan Hesabı 1 log grubuna erişemedi. Asistanı log grubuna eklediğinizden ve yönetici yetkisi verdiğinizden emin olun!"
                )
                exit()
            self.one.id = self.one.me.id
            self.one.name = self.one.me.mention
            self.one.username = self.one.me.username
            assistantids.append(self.one.id)
            LOGGER(__name__).info(f"Asistan {self.one.name} olarak başlatıldı")

        if config.STRING2:
            await self.two.start()
            assistants.append(2)
            try:
                await self.two.send_message(config.LOGGER_ID, "Asistan Başlatıldı")
            except:
                LOGGER(__name__).error(
                    "Asistan Hesabı 2 log grubuna erişemedi. Asistanı log grubuna eklediğinizden ve yönetici yetkisi verdiğinizden emin olun!"
                )
                exit()
            self.two.id = self.two.me.id
            self.two.name = self.two.me.mention
            self.two.username = self.two.me.username
            assistantids.append(self.two.id)
            LOGGER(__name__).info(f"Asistan İki {self.two.name} olarak başlatıldı")

        if config.STRING3:
            await self.three.start()
            assistants.append(3)
            try:
                await self.three.send_message(config.LOGGER_ID, "Asistan Başlatıldı")
            except:
                LOGGER(__name__).error(
                    "Asistan Hesabı 3 log grubuna erişemedi. Asistanı log grubuna eklediğinizden ve yönetici yetkisi verdiğinizden emin olun!"
                )
                exit()
            self.three.id = self.three.me.id
            self.three.name = self.three.me.mention
            self.three.username = self.three.me.username
            assistantids.append(self.three.id)
            LOGGER(__name__).info(f"Asistan Üç {self.three.name} olarak başlatıldı")

        if config.STRING4:
            await self.four.start()
            assistants.append(4)
            try:
                await self.four.send_message(config.LOGGER_ID, "Asistan Başlatıldı")
            except:
                LOGGER(__name__).error(
                    "Asistan Hesabı 4 log grubuna erişemedi. Asistanı log grubuna eklediğinizden ve yönetici yetkisi verdiğinizden emin olun!"
                )
                exit()
            self.four.id = self.four.me.id
            self.four.name = self.four.me.mention
            self.four.username = self.four.me.username
            assistantids.append(self.four.id)
            LOGGER(__name__).info(f"Asistan Dört {self.four.name} olarak başlatıldı")

        if config.STRING5:
            await self.five.start()
            assistants.append(5)
            try:
                await self.five.send_message(config.LOGGER_ID, "Asistan Başlatıldı")
            except:
                LOGGER(__name__).error(
                    "Asistan Hesabı 5 log grubuna erişemedi. Asistanı log grubuna eklediğinizden ve yönetici yetkisi verdiğinizden emin olun!"
                )
                exit()
            self.five.id = self.five.me.id
            self.five.name = self.five.me.mention
            self.five.username = self.five.me.username
            assistantids.append(self.five.id)
            LOGGER(__name__).info(f"Asistan Beş {self.five.name} olarak başlatıldı")

    async def stop(self):
        LOGGER(__name__).info("Asistanlar Durduruluyor...")
        try:
            if config.STRING1:
                await self.one.stop()
            if config.STRING2:
                await self.two.stop()
            if config.STRING3:
                await self.three.stop()
            if config.STRING4:
                await self.four.stop()
            if config.STRING5:
                await self.five.stop()
        except:
            pass
