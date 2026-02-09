#
# Copyright (C) 2021-2022 by TheAloneteam@Github, < https://github.com/TheAloneTeam >.
#
# This file is part of < https://github.com/TheAloneTeam/AloneMusic > project,
# and is released under the "GNU v3.0 License Agreement".
# Please see < https://github.com/TheAloneTeam/AloneMusic/blob/master/LICENSE >
#
# All rights reserved.

from typing import Union

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from AloneMusic import app


def help_pannel(_, START: Union[bool, int] = None):
    # Kapat butonu (Eğer direkt yardım menüsündeyse)
    first = [InlineKeyboardButton(text=_["CLOSE_BUTTON"], callback_data="close")]

    # Geri butonu (Eğer ayarlar üzerinden geldiyse)
    second = [
        InlineKeyboardButton(
            text=_["BACK_BUTTON"],
            callback_data="settings_back_helper",  # Yazım hatası düzeltildi
        ),
    ]

    # START parametresine göre hangi alt butonun gösterileceği seçilir
    mark = second if START else first

    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["H_B_1"],
                    callback_data="help_callback hb1",
                ),
                InlineKeyboardButton(
                    text=_["H_B_2"],
                    callback_data="help_callback hb2",
                ),
                InlineKeyboardButton(
                    text=_["H_B_3"],
                    callback_data="help_callback hb3",
                ),
            ],
            mark,
        ]
    )
    return upl


def help_back_markup(_):
    upl = InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(
                    text=_["BACK_BUTTON"],
                    callback_data="settings_back_helper",
                ),
            ]
        ]
    )
    return upl


def private_help_panel(_):
    buttons = [
        [
            InlineKeyboardButton(
                text=_["S_B_4"],
                url=f"https://t.me/{app.username}?start=help",
            ),
        ],
    ]
    return buttons
