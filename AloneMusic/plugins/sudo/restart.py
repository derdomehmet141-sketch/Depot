
import asyncio
import os
import shutil
import socket
from datetime import datetime

import urllib3
from git import Repo
from git.exc import GitCommandError, InvalidGitRepositoryError
from pyrogram import filters

import config
from AloneMusic import app
from AloneMusic.misc import HAPP, SUDOERS, XCB
from AloneMusic.utils.database import (get_active_chats, remove_active_chat,
                                       remove_active_video_chat)
from AloneMusic.utils.decorators.language import language

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


async def is_heroku():
    return "heroku" in socket.getfqdn().lower()


# ---------------- LOGLAR ----------------
@app.on_message(filters.command(["getlog", "logs", "getlogs", "loglar"]) & SUDOERS)
@language
async def log_(client, message, _):
    try:
        await message.reply_document("log.txt")
    except:
        await message.reply_text("Log dosyası bulunamadı veya gönderilemedi.")


# ---------------- GÜNCELLEME ----------------
@app.on_message(filters.command(["update", "gitpull", "guncelle"]) & SUDOERS)
@language
async def update_(client, message, _):
    if await is_heroku():
        if HAPP is None:
            return await message.reply_text("Heroku yapılandırması eksik, güncelleme yapılamıyor.")

    response = await message.reply_text("Güncellemeler kontrol ediliyor, lütfen bekleyin...")

    try:
        repo = Repo(search_parent_directories=True)
    except GitCommandError:
        return await response.edit("Git komut hatası oluştu.")
    except InvalidGitRepositoryError:
        return await response.edit("Geçersiz Git deposu.")

    os.system(f"git fetch origin {config.UPSTREAM_BRANCH} &> /dev/null")
    await asyncio.sleep(5)

    verification = ""
    for check in repo.iter_commits(f"HEAD..origin/{config.UPSTREAM_BRANCH}"):
        verification = str(check.count())

    if verification == "":
        return await response.edit("Bot zaten en güncel sürümde.")

    updates = ""
    REPO_ = repo.remotes.origin.url.split(".git")[0]

    def ordinal(n):
        return "%d." % n  # Türkçe için sadece nokta yeterlidir

    for info in repo.iter_commits(f"HEAD..origin/{config.UPSTREAM_BRANCH}"):
        date = datetime.fromtimestamp(info.committed_date)
        updates += (
            f"<b>➣ #{info.count()}: "
            f"<a href={REPO_}/commit/{info}>{info.summary}</a> "
            f"Yazılım: {info.author}</b>\n"
            f"\t\t<b>➥ Tarih:</b> "
            f"{date.strftime('%d')} "
            f"{date.strftime('%b')}, {date.strftime('%Y')}\n\n"
        )

    final_text = (
        "<b>Bot için yeni bir güncelleme mevcut!</b>\n\n"
        "➣ Güncellemeler uygulanıyor...\n\n"
        "<b><u>Değişiklikler:</u></b>\n\n"
        f"{updates}"
    )

    await response.edit(final_text, disable_web_page_preview=True)

    os.system("git stash &> /dev/null && git pull &> /dev/null")

    try:
        chats = await get_active_chats()
        for x in chats:
            try:
                await app.send_message(
                    int(x),
                    f"{app.mention} güncelleniyor. Görüşmek üzere!",
                )
                await remove_active_chat(x)
                await remove_active_video_chat(x)
            except:
                pass

        await response.edit(f"{final_text}\n\nBot başarıyla güncellendi! Yeniden başlatılıyor...")
    except:
        pass

    # -------- YENİDEN BAŞLAT --------
    if await is_heroku():
        try:
            os.system(
                f"{XCB[5]} {XCB[7]} {XCB[9]}{XCB[4]}{XCB[0]*2}{XCB[6]}"
                f"{XCB[4]}{XCB[8]}{XCB[1]}{XCB[5]}{XCB[2]}"
                f"{XCB[6]}{XCB[2]}{XCB[3]}{XCB[0]}"
                f"{XCB[10]}{XCB[2]}{XCB[5]} "
                f"{XCB[11]}{XCB[4]}{XCB[12]}"
            )
            return
        except Exception as err:
            await app.send_message(
                config.LOGGER_ID,
                f"Güncelleme sırasında hata oluştu: {err}",
            )
    else:
        os.system("uv pip install -e .")
        os.system(f"kill -9 {os.getpid()} && python3 -m AloneMusic")


# ---------------- YENİDEN BAŞLAT ----------------
@app.on_message(filters.command(["restart", "yenidenbaslat"]) & SUDOERS)
async def restart_(_, message):
    response = await message.reply_text("Yeniden başlatılıyor...")

    chats = await get_active_chats()
    for x in chats:
        try:
            await app.send_message(
                int(x),
                f"{app.mention} yeniden başlatılıyor...\n\n"
                "15-20 saniye sonra tekrar çalmaya "
                "başlayabilirsiniz.",
            )
            await remove_active_chat(x)
            await remove_active_video_chat(x)
        except:
            pass

    for folder in ("downloads", "raw_files", "cache"):
        if os.path.exists(folder):
            shutil.rmtree(folder, ignore_errors=True)

    await response.edit("» Yeniden başlatma işlemi başladı, lütfen bekleyin...")
    os.system(f"kill -9 {os.getpid()} && python3 -m AloneMusic")
