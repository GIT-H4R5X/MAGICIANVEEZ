""" broadcast & statistic collector """

import asyncio

from pyrogram.types import Message
from pyrogram import Client, filters, __version__ as pyrover

from pytgcalls import (__version__ as pytgver)

from program import __version__ as ver
from program.start import __python_version__ as pyver

from driver.filters import command
from driver.decorators import sudo_users_only
from driver.database.dbchat import get_served_chats
from driver.database.dbusers import get_served_users
from driver.database.dbpunish import get_gbans_count

from config import BOT_NAME as name, BOT_USERNAME as uname


@Client.on_message(command(["broadcast", f"broadcast@{uname}"]) & ~filters.edited)
@sudo_users_only
async def broadcast(c: Client, message: Message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await c.forward_messages(i, y, x)
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(f"✅ Broadcast complete in {sent} Group.")
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**usage**:\n\n/broadcast (`message`) or (`reply to message`)"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await c.send_message(i, text=text)
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(f"✅ Broadcast complete in {sent} Group.")


@Client.on_message(command(["broadcast_pin", f"broadcast_pin@{uname}"]) & ~filters.edited)
@sudo_users_only
async def broadcast_pin(c: Client, message: Message):
    if not message.reply_to_message:
        pass
    else:
        x = message.reply_to_message.message_id
        y = message.chat.id
        sent = 0
        pin = 0
        chats = []
        schats = await get_served_chats()
        for chat in schats:
            chats.append(int(chat["chat_id"]))
        for i in chats:
            try:
                m = await c.forward_messages(i, y, x)
                try:
                    await m.pin(disable_notification=True)
                    pin += 1
                except Exception:
                    pass
                await asyncio.sleep(0.3)
                sent += 1
            except Exception:
                pass
        await message.reply_text(
            f"✅ Broadcast complete in {sent} Group.\n📌 With the {pin} pins."
        )
        return
    if len(message.command) < 2:
        await message.reply_text(
            "**usage**:\n\n/broadcast (`message`) or (`reply to message`)"
        )
        return
    text = message.text.split(None, 1)[1]
    sent = 0
    pin = 0
    chats = []
    schats = await get_served_chats()
    for chat in schats:
        chats.append(int(chat["chat_id"]))
    for i in chats:
        try:
            m = await c.send_message(i, text=text)
            try:
                await m.pin(disable_notification=True)
                pin += 1
            except Exception:
                pass
            await asyncio.sleep(0.3)
            sent += 1
        except Exception:
            pass
    await message.reply_text(
        f"✅ Broadcast complete in {sent} Group.\n📌 With the {pin} pins."
    )


@Client.on_message(command(["stats", f"stats@{uname}"]) & ~filters.edited)
@sudo_users_only
async def broadcast(c: Client, message: Message):
    chat_id = message.chat.id
    user_id = message.from_user.id
    msg = await c.send_message(
        chat_id, "🔄 `Calculating statistic...`"
    )
    served_chats = len(await get_served_chats())
    served_users = len(await get_served_users())
    gbans_usertl = await get_gbans_count()
    tgm = f"""
📊 Current Statistic of [{name}]({uname})`:`

➥ **Groups Chat** : `{served_chats}`
➥ **Users Dialog** : `{served_users}`
➥ **Gbanned Users** : `{gbans_usertl}`

➛ **Python Version** : `{pyver}`
➛ **PyTgCalls Version** : `{pytgver}`
➛ **Pyrogram Version** : `{pyrover}`

🤖 bot version: `{ver}`"""
    
    await msg.edit(tgm, disable_web_page_preview=True)
