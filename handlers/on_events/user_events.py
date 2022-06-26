from pathlib import Path

import discord
from fuzzywuzzy import fuzz

from data.config import PREFIX
from loader import bot
from utils.db_stuff.db_functions import add_user, add_spam_warns, get_warns, null_warns, add_xp_to_user
from utils.channel_roles import admin_roles


@bot.event
async def on_member_join(member):
    """Функция on_member_join добавляет в бд имя, id, количество
    xp и сервер пользователя, если его ещё нет в бд."""

    await add_user(member, member.id)


@bot.event
async def on_message(message):
    """Функция on_message проверяет содержимое отправляемых сообщений на
    наличие спама и мата. Если спам и мат обнаруживается в них, то юзеру
    выдаётся предупрежедние, которое вноситься в бд. Если у юзера больше 5 предупреждений
    за мат или больше 3 предупреждений за спам, то пользователя кикают или мутят."""

    if message.content.startswith(PREFIX):
        await bot.process_commands(message)

    else:
        muted_role = message.author.guild.get_role(970187622179831878)
        channel = bot.get_channel(message.channel.id)

        if message.author.id not in admin_roles:
            if len(message.content) > 16:
                messages = await channel.history(limit=100, oldest_first=False).flatten()
                spams_msgs = []
                spams = 0

                for msg in messages:
                    if msg.author.id == message.author.id and not message.author.bot \
                            and fuzz.ratio(msg.content.lower(), message.content.lower()) > 90:
                        spams_msgs.append(msg)
                        spams += 1

                if spams > 1:
                    await add_spam_warns(message.author.id)

                    num_warns = await get_warns(message.author.id)
                    emb = discord.Embed(title=f"{message.author}, не спамь! Тебе было выдано предупреждение. "
                                              f"Всего предупреждений: {num_warns}. Ты получишь мут на"
                                              f" неопределённый срок, если у тебя будет больше 3 предупреждений!",
                                        colour=discord.Colour.red())
                    await channel.send(embed=emb)

                    for msg in spams_msgs:
                        await msg.delete()

            num_warns = await get_warns(message.author.id)

            if num_warns >= 3:
                emb = discord.Embed(title=f"Пользователь {message.author} был отправлен в Азкабан.",
                                    colour=discord.Colour.red())
                await channel.send(embed=emb)

                for role in message.author.roles:
                    if role.id != 770696230790627398:
                        await message.author.remove_roles(role)

                await message.author.add_roles(muted_role)

                await null_warns(message.author.id)

            words = message.content.replace(",.?!&\"\':;", "").lower().split(" ")

            path = Path("utils", "misc", "bad_words.txt")

            with open(path, "r", encoding="utf-8") as bad_words:
                for word in words:
                    for bad in bad_words:
                        equal = fuzz.ratio(word, bad.lower())

                        if equal > 75:
                            await message.delete()
                            emb = discord.Embed(
                                title=f"{message.author}, дементоры обнаружили мат на территории Хогвартса!",
                                colour=discord.Colour.red())
                            await channel.send(embed=emb)


@bot.event
async def on_raw_reaction_add(payload):
    """Функция on_raw_reaction_add прибавляет к полю xp в бд 500,
    если сообщение пользователя было помечено реакцией '👍'.
    """

    channel = bot.get_channel(payload.channel_id)
    message = await channel.fetch_message(payload.message_id)
    guild = bot.get_guild(payload.guild_id)

    reaction = discord.utils.get(message.reactions, emoji=payload.emoji.name)

    if payload.member.id == 724937739623202816 and str(reaction.emoji) == '👍':
        msg = await bot.get_channel(payload.channel_id).fetch_message(payload.message_id)
        member = msg.author

        await add_xp_to_user(10, member.id)