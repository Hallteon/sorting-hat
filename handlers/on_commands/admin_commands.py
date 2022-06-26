import asyncio

import discord
from discord.ext import commands

from loader import bot
from utils.db_stuff.db_functions import add_xp_to_user, remove_xp_from_user
from utils.channel_roles import admin_roles


@bot.command()
@commands.has_any_role(*admin_roles)
async def add_xp(ctx, member: discord.Member = None, xp: int = None):
    """Функция add_xp прибавляет к полю xp пользователя указанное число xp.
    (только для админов).
    """

    if member is None:
        emb = discord.Embed(title="Укажите пользователя!", colour=discord.Colour.red())
        await ctx.send(embed=emb)

    else:
        if xp is None:
            emb = discord.Embed(title="Укажите количество XP!", colour=discord.Colour.red())
            await ctx.send(embed=emb)

        elif xp < 0:
            emb = discord.Embed(title="Укажите положительное число XP!", colour=discord.Colour.red())
            await ctx.send(embed=emb)

        elif xp >= 2147483647:
            emb = discord.Embed(title="Вы указали слишком большое число XP!", colour=discord.Colour.red())
            await ctx.send(embed=emb)

        else:
            emb = discord.Embed(title=f"Пользователю {member} добавлено {xp}XP.", colour=discord.Colour.green())

            await add_xp_to_user(xp, member.id)
            await ctx.send(embed=emb)

    await ctx.message.delete()


@bot.command()
@commands.has_any_role(*admin_roles)
async def remove_xp(ctx, member: discord.Member = None, xp: int = None):
    """Функция remove_xp вычитает из поля xp пользователя указанное число xp.
    (только для админов).
    """

    if member is None:
        emb = discord.Embed(title="Укажите пользователя!", colour=discord.Colour.red())
        await ctx.send(embed=emb)

    else:
        if xp is None:
            emb = discord.Embed(title="Укажите количество XP!", colour=discord.Colour.red())
            await ctx.send(embed=emb)

        elif xp < 0:
            emb = discord.Embed(title="Укажите положительное число XP!", colour=discord.Colour.red())
            await ctx.send(embed=emb)

        elif xp >= 2147483647:
            emb = discord.Embed(title="Вы указали слишком большое число XP!", colour=discord.Colour.red())
            await ctx.send(embed=emb)

        else:
            emb = discord.Embed(title=f"У пользователя {member} отнято {xp}XP.", colour=discord.Colour.green())
            await ctx.send(embed=emb)

            await remove_xp_from_user(xp, member.id)

    await ctx.message.delete()


@bot.command()
@commands.has_any_role(*admin_roles)
async def kick(ctx, member: discord.Member, *, reason=None):
    """Функция kick удаляет пользователя member с сервера.
    (только для админа).
    """
    if ctx.message.author.guild.id == 770696230790627398:
        if member:
            emb = discord.Embed(title=f"Пользователь {member} был кикнут.", colour=discord.Colour.orange())
            await ctx.channel.purge(limit=1)
            await member.kick(reason=reason)
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(title="Укажите пользователя!", colour=discord.Colour.red())
            await ctx.send(embed=emb)
    else:
        emb = discord.Embed(title="Эта команда не работает на этом сервере!", colour=discord.Colour.red())
        await ctx.send(embed=emb)


@bot.command()
@commands.has_any_role(*admin_roles)
async def mute(ctx, member: discord.Member, time: int, reason=None):
    """Функция mute ограничивает доступ пользователя member к чату
    на указанное время.
    (только для админов)
    """
    if ctx.message.author.guild.id == 770696230790627398:
        role = discord.utils.get(ctx.channel.guild.roles, id=906439766390747146)
        await ctx.channel.purge(limit=1)
        if role in member.roles:
            emb = discord.Embed(title=f"Пользователю {member} уже выдан мут.", colour=discord.Colour.red())
            await ctx.send(embed=emb)
        else:
            emb = discord.Embed(title=f"Пользователь {member} получил мут на {time} минут по причине: {reason}.",
                                colour=discord.Colour.red())
            await member.add_roles(role)
            await ctx.send(embed=emb)
            await member.move_to(None)
            await asyncio.sleep(time * 60)
            await member.remove_roles(role)
    else:
        emb = discord.Embed(title="Эта команда не работает на этом сервере!", colour=discord.Colour.red())
        await ctx.send(embed=emb)


@bot.command()
@commands.has_any_role(*admin_roles)
async def ban(ctx, member: discord.Member, *, reason=None):
    """Функция ban ограничивает доступ пользователя member к серверу.
    (только для админов).
    """
    if ctx.message.author.guild.id == 770696230790627398:
        if member:
            if reason:
                emb = discord.Embed(title=f"Пользователь {member} был забанен по причине: {reason}.",
                                    colour=discord.Colour.red())
                await ctx.channel.purge(limit=1)
                await member.ban(reason=reason)
                await ctx.send(embed=emb)
            else:
                emb = discord.Embed(title=f"Укажите причину!", colour=discord.Colour.red())
                await ctx.send(embed=emb)
        else:
            emb = discord.Embed(title=f"Укажите пользователя!", colour=discord.Colour.red())
            await ctx.send(embed=emb)
    else:
        emb = discord.Embed(title="Эта команда не работает на этом сервере!", colour=discord.Colour.red())
        await ctx.send(embed=emb)


@bot.command()
@commands.has_any_role(*admin_roles)
async def clear(ctx, amount=10):
    """Функция clear удаляет указанное колличество сообщения
    из чата (по умолчанию 1000).
    (только для админов).
    """
    if ctx.message.author.guild.id == 770696230790627398:
        await ctx.channel.purge(limit=amount + 1)
    else:
        emb = discord.Embed(title="Эта команда не работает на этом сервере!", colour=discord.Colour.red())
        await ctx.send(embed=emb)