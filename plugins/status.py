from datetime import datetime
from info import CHANNELS
from plugins.database import db
from utils import is_group_exist
async def handle_user_status(bot, cmd):
    chat_id = cmd.from_user.id if cmd.from_user else None
    if chat_id:
        if not await db.is_user_exist(chat_id):
            await db.add_user(chat_id)
            await bot.send_message(
                chat_id= CHANNELS,
                text=f"#NEW_USER: \n\nNew User [{cmd.from_user.first_name}](tg://user?id={cmd.from_user.id}) started!!"
            )

        ban_status = await db.get_ban_status(chat_id)
        if cmd.chat.type == "private":
            return
        if ban_status["is_banned"]:
            if (
                    datetime.now() > ban_status["banned_on"]
            ):
                await db.remove_ban(chat_id)
                await db.update_ban(id,'Siku 0,00:00:00')
            else:
                await db.update_ban(id,f'Siku {(ban_status["banned_on"]-datetime.now()).days},{(ban_status["banned_on"]-datetime.now()).hours}:{(ban_status["banned_on"]-datetime.now()).minutes}:{(ban_status["banned_on"]-datetime.now()).seconds}')
        if await is_group_exist(cmd.chat.id):
            await db.update_grd_id(chat_id,cmd.chat.id)
        else:
            await db.update_grd_id(chat_id,0)


