from telethon.tl.types import Channel

from telebot import *
from telebot import ALIVE_NAME, bot, telever
from telebot.telebotConfig import Config, Var

# stats
if Var.PRIVATE_GROUP_ID:
    log = "Enabled"
else:
    log = "Disabled"

if Config.TG_BOT_USER_NAME_BF_HER:
    bots = "Enabled"
else:
    bots = "Disabled"

if Var.LYDIA_API_KEY:
    lyd = "Enabled"
else:
    lyd = "Disabled"

if Config.SUDO_USERS:
    sudo = "Disabled"
else:
    sudo = "Enabled"

if Var.PMSECURITY.lower() == "off":
    pm = "Disabled"
else:
    pm = "Enabled"

TELEUSER = str(ALIVE_NAME) if ALIVE_NAME else "@TeleBotSupport"

tele = f"TeleBot Version: {telever}\n"
tele += f"Log Group: {log}\n"
tele += f"Assistant Bot: {bots}\n"
tele += f"Lydia: {lyd}\n"
tele += f"Sudo: {sudo}\n"
tele += f"PMSecurity: {pm}\n"
tele += f"\nVisit @TeleBotSupport for assistance.\n"
telestats = f"{tele}"

TELE_NAME = bot.me.first_name
OWNER_ID = bot.me.id

# count total number of groups


async def tele_grps(event):
    a = []
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel):
            if entity.megagroup:
                if entity.creator or entity.admin_rights:
                    a.append(entity.id)
    return len(a), a
