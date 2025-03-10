from functools import wraps


from pyrogram import enums
from pyrogram.types import Message
import loguru

from . import bot as app
from . import env
loguru.logger.info(env.channel_id)


async def is_user_a_member_of_channel(bot: app, message: Message) -> bool:
    user = await bot.get_chat_member(
        int(env.channel_id), message.from_user.id
    )
    return user.status in [
        enums.ChatMemberStatus.ADMINISTRATOR,
        enums.ChatMemberStatus.MEMBER,
        enums.ChatMemberStatus.OWNER,
    ]


async def is_not_user_a_member_of_channel(bot: app, message: Message) -> bool:
    return not await is_user_a_member_of_channel(bot, message)
