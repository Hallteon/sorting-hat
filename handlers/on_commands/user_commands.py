from discord_components import ButtonStyle, Button

from data.config import PREFIX
from loader import bot

from utils.db_stuff.db_functions import select_xp, select_top_users
from utils.channel_roles import roles
from utils.misc.select_faculty_stuff import *


@bot.command()
async def help(ctx):
    """Функция help возвращает список команд бота, для обычных пользователей -
    select_faculty, top и xp, а для админа ещё и add_xp, kick, ban,
    clear.
    """

    emb = discord.Embed(title="Навигация по командам:", colour=discord.Colour.orange())

    if ctx.message.author.guild.id == 770696230790627398:
        emb.add_field(name=f"{PREFIX}select_faculty", value="Выбрать факультет.", inline=False)

        if map(lambda role: role.id == 774190806583607376, ctx.message.author.roles):
            emb.add_field(name=f"{PREFIX}add_xp", value="Добавить опыт участнику.", inline=False)
            emb.add_field(name=f"{PREFIX}remove_xp", value="Забрать опыт у участника.", inline=False)

        elif ctx.message.author.id == 724937739623202816:
            emb.add_field(name=f"{PREFIX}add_xp", value="Добавить опыт участнику.", inline=False)
            emb.add_field(name=f"{PREFIX}remove_xp", value="Забрать опыт у участника.", inline=False)
            emb.add_field(name=f"{PREFIX}mute", value="Выдать участнику мут на время.", inline=False)
            emb.add_field(name=f"{PREFIX}kick", value="Удалить участника с сервера.", inline=False)
            emb.add_field(name=f"{PREFIX}ban", value="Ограничить доступ участника к серверу.", inline=False)
            emb.add_field(name=f"{PREFIX}clear", value="Удалить сообщения (по умолчанию 10).")

    emb.add_field(name=f"{PREFIX}top", value="Топ 10 участников сервера по опыту.", inline=False)
    emb.add_field(name=f"{PREFIX}xp", value="Узнать ваш опыт.", inline=False)
    emb.set_footer(text="Brainstorm1451#2132 © 2021")
    await ctx.send(embed=emb)


@bot.command(aliases=["xp"])
async def get_xp(ctx, member: discord.Member = None):
    """Функция get_xp возвращает твоё колличсетво xp, если member
    не был указан, и количество xp другого пользователя, если был.
    """

    if member:
        xp = await select_xp(member.id)
        emb = discord.Embed(title=f"У пользователя **{member} {xp}XP**.",
                            colour=discord.Colour.green())

        await ctx.send(embed=emb)

    else:
        xp = await select_xp(ctx.author.id)
        emb = discord.Embed(title=f"{ctx.author}, у вас **{xp}XP**.",
                            colour=discord.Colour.green())

        await ctx.send(embed=emb)


@bot.command()
async def top(ctx):
    """Функция top возвращает список топ 10 участников сервера по
    колличеству xp.
    """

    emb = discord.Embed(title="Топ 10 участников сервера:")
    top_users = await select_top_users()
    counter = 0

    for row in top_users:
        counter += 1
        emb.add_field(
            name=f"{counter}. {row[0]}",
            value=f"Опыт: {row[1]}XP",
            inline=False
        )

    await ctx.send(embed=emb)


@bot.command()
async def select_faculty(ctx):
    """Функция select_faculty позволяет выбрать сразу или пройти тест для
    определения факультета.
    """

    member = ctx.message.author

    if member.guild.id == 770696230790627398:

        send_fac_menu = ctx.send(embed=select_fac_emb, components=[
            [Button(style=ButtonStyle.green, label="Гриффиндор", emoji="🦁"),
             Button(style=ButtonStyle.blue, label="Слизерин", emoji="🐍")],
            [Button(style=ButtonStyle.red, label="Когтевран", emoji="🦝"),
             Button(style=ButtonStyle.gray, label="Пуффендуй", emoji="🦅")],
            [Button(style=ButtonStyle.blue, label="Пожиратели Смерти", emoji="💀")]
        ])

        answer = await ctx.channel.send(embed=start_emb, components=[[
            Button(style=ButtonStyle.green, label="Выбрать сразу"),
            Button(style=ButtonStyle.blue, label="Пройти тест")]])

        response = await bot.wait_for("button_click", check=lambda message: message.author == ctx.author)
        await response.edit_origin()

        if response.component.label == "Выбрать сразу":
            for role in [role.name for role in ctx.author.roles]:
                if role != "@everyone" and role.lower() in channel_roles:
                    user_role = discord.utils.get(ctx.message.author.roles, name=role)
                    await member.remove_roles(user_role)

            await ctx.message.delete()
            await answer.delete()

            faculty = ""
            answer = await ctx.send(embed=who_emb, components=[
                [Button(style=ButtonStyle.green, label="Ученик с жаждой знаний", emoji="👨‍🎓")],
                [Button(style=ButtonStyle.blue, label="Мудрый наставник", emoji="🧙")]
            ])

            response = await bot.wait_for("button_click", check=lambda message: message.author == ctx.author)
            await response.edit_origin()

            if response.component.label == "Ученик с жаждой знаний":
                await answer.delete()

                answer = await send_fac_menu

                response = await bot.wait_for("button_click", check=lambda message: message.author == ctx.author)
                await response.edit_origin()

                if response.component.label == "Гриффиндор":
                    faculty = "gryff"
                    await member.add_roles(discord.utils.get(ctx.channel.guild.roles, id=roles["apprentice"]["gryff"])
                                           )
                elif response.component.label == "Слизерин":
                    faculty = "slyth"
                    await member.add_roles(discord.utils.get(ctx.channel.guild.roles, id=roles["apprentice"]["slyth"]))
                elif response.component.label == "Когтевран":

                    faculty = "raven"
                    await member.add_roles(discord.utils.get(ctx.channel.guild.roles, id=roles["apprentice"]["raven"]))
                elif response.component.label == "Пуффендуй":

                    faculty = "huff"
                    await member.add_roles(discord.utils.get(ctx.channel.guild.roles, id=roles["apprentice"]["huff"]))
                elif response.component.label == "Пожиратели Смерти":

                    faculty = "death"
                    await member.add_roles(discord.utils.get(ctx.channel.guild.roles, id=roles["apprentice"]["death"]))

                await member.add_roles(discord.utils.get(ctx.channel.guild.roles, id=roles["apprentice"]["apprentice"]))
                await answer.delete()

            elif response.component.label == "Мудрый наставник":
                await answer.delete()

                answer = await send_fac_menu

                response = await bot.wait_for("button_click", check=lambda message: message.author == ctx.author)
                await response.edit_origin()

                if response.component.label == "Гриффиндор":
                    faculty = "gryff"
                    await member.add_roles(discord.utils.get(ctx.channel.guild.roles, id=roles["mentor"]["gryff"]))

                elif response.component.label == "Слизерин":
                    faculty = "slyth"
                    await member.add_roles(discord.utils.get(ctx.channel.guild.roles, id=roles["mentor"]["slyth"]))

                elif response.component.label == "Когтевран":
                    faculty = "raven"
                    await member.add_roles(discord.utils.get(ctx.channel.guild.roles, id=roles["mentor"]["raven"]))

                elif response.component.label == "Пуффендуй":
                    faculty = "huff"
                    await member.add_roles(discord.utils.get(ctx.channel.guild.roles, id=roles["mentor"]["huff"]))

                elif response.component.label == "Пожиратели Смерти":
                    faculty = "death"
                    await member.add_roles(discord.utils.get(ctx.channel.guild.roles, id=roles["mentor"]["death"]))

                await member.add_roles(discord.utils.get(ctx.channel.guild.roles, id=roles["mentor"]["mentor"]))
                await answer.delete()

            emb = discord.Embed(title=f"Пользователь {member} зачислен в {names_faculties[faculty]}!",
                                colour=discord.Colour.green())
            await ctx.send(embed=emb)

        elif response.component.label == "Пройти тест":
            faculties = {
                "gryff": 0,
                "slyth": 0,
                "huff": 0,
                "raven": 0,
                "death": 0
            }

            who = ""
            faculty = ""

            await ctx.message.delete()
            await answer.delete()

            answer = await member.send(embed=who_emb, components=[
                [Button(style=ButtonStyle.green, label="Ученик с жаждой знаний", emoji="👨‍🎓")],
                [Button(style=ButtonStyle.blue, label="Мудрый наставник", emoji="🧙")]
            ])

            response = await bot.wait_for("button_click", check=lambda message: message.author == ctx.author)
            await response.edit_origin()

            if response.component.label == "Ученик с жаждой знаний":
                who = "apprentice"

            elif response.component.label == "Мудрый наставник":
                who = "mentor"

            await answer.delete()

            answer = await member.send(embed=question1_emb, components=[
                [Button(style=ButtonStyle.red, label="Храбрый"),
                 Button(style=ButtonStyle.green, label="Хитрый"),
                 Button(style=ButtonStyle.gray, label="Упорный")],
                [Button(style=ButtonStyle.blue, label="Мудрый"),
                 Button(style=ButtonStyle.gray, label="Злорадный")]
            ])

            response = await bot.wait_for("button_click", check=lambda message: message.author == ctx.author)
            await response.edit_origin()

            if response.component.label == "Храбрый":
                faculties["gryff"] += 1

            elif response.component.label == "Хитрый":
                faculties["slyth"] += 1

            elif response.component.label == "Упорный":
                faculties["huff"] += 1

            elif response.component.label == "Мудрый":
                faculties["raven"] += 1

            elif response.component.label == "Злорадный":
                faculties["death"] += 1

            await answer.delete()

            answer = await member.send(embed=question2_emb, components=[
                [Button(style=ButtonStyle.red, label="Лев"),
                 Button(style=ButtonStyle.green, label="Змея"),
                 Button(style=ButtonStyle.gray, label="Барсук"),
                 Button(style=ButtonStyle.blue, label="Орёл")],
                [Button(style=ButtonStyle.gray, label="Летучая мышь")]
            ])

            response = await bot.wait_for("button_click", check=lambda message: message.author == ctx.author)
            await response.edit_origin()

            if response.component.label == "Лев":
                faculties["gryff"] += 1

            elif response.component.label == "Змея":
                faculties["slyth"] += 1

            elif response.component.label == "Барсук":
                faculties["huff"] += 1

            elif response.component.label == "Орёл":
                faculties["raven"] += 1

            elif response.component.label == "Летучая мышь":
                faculties["death"] += 1

            await answer.delete()

            answer = await member.send(embed=question3_emb, components=[
                [Button(style=ButtonStyle.red, label="Огонь"),
                 Button(style=ButtonStyle.green, label="Вода"),
                 Button(style=ButtonStyle.gray, label="Земля"),
                 Button(style=ButtonStyle.blue, label="Воздух")],
                [Button(style=ButtonStyle.gray, label="Хаос")]
            ])

            response = await bot.wait_for("button_click", check=lambda message: message.author == ctx.author)
            await response.edit_origin()

            if response.component.label == "Огонь":
                faculties["gryff"] += 1

            elif response.component.label == "Вода":
                faculties["slyth"] += 1

            elif response.component.label == "Земля":
                faculties["huff"] += 1

            elif response.component.label == "Воздух":
                faculties["raven"] += 1

            elif response.component.label == "Хаос":
                faculties["death"] += 1

            await answer.delete()

            answer = await member.send(embed=question4_emb, components=[
                [Button(style=ButtonStyle.red, label="Красный и жёлтый"),
                 Button(style=ButtonStyle.green, label="Зелёный и серебрянный")],
                [Button(style=ButtonStyle.gray, label="Жёлтый и чёрный"),
                 Button(style=ButtonStyle.blue, label="Синий и бронзовый")],
                [Button(style=ButtonStyle.green, label="Зелёный и чёрный")]
            ])

            response = await bot.wait_for("button_click", check=lambda message: message.author == ctx.author)
            await response.edit_origin()

            if response.component.label == "Красный и жёлтый":
                faculties["gryff"] += 1

            elif response.component.label == "Зелёный и серебрянный":
                faculties["slyth"] += 1

            elif response.component.label == "Жёлтый и чёрный":
                faculties["huff"] += 1

            elif response.component.label == "Синий и бронзовый":
                faculties["raven"] += 1

            elif response.component.label == "Зелёный и чёрный":
                faculties["death"] += 1

            await answer.delete()

            answer = await member.send(embed=question5_emb, components=[
                [Button(style=ButtonStyle.red, label="Почти Безголовый Ник"),
                 Button(style=ButtonStyle.green, label="Кровавый Барон")],
                [Button(style=ButtonStyle.gray, label="Толстый Монах"),
                 Button(style=ButtonStyle.blue, label="Серая Дама")],
                [Button(style=ButtonStyle.green, label="Не люблю призраков")]
            ])

            response = await bot.wait_for("button_click", check=lambda message: message.author == ctx.author)
            await response.edit_origin()

            if response.component.label == "Почти Безголовый Ник":
                faculties["gryff"] += 1

            elif response.component.label == "Кровавый Барон":
                faculties["slyth"] += 1

            elif response.component.label == "Толстый Монах":
                faculties["huff"] += 1

            elif response.component.label == "Серая Дама":
                faculties["raven"] += 1

            elif response.component.label == "Не люблю призраков":
                faculties["death"] += 1

            await answer.delete()

            for k, v in faculties.items():
                if v == max(faculties.values()):
                    faculty = k

            for role in [role.name for role in ctx.author.roles]:
                if role != "@everyone" and role.lower() in channel_roles:
                    user_role = discord.utils.get(ctx.message.author.roles, name=role)
                    await member.remove_roles(user_role)

            emb = discord.Embed(title=f"Вы зачислены в {names_faculties[faculty]}!", colour=discord.Colour.green())

            await member.send(embed=emb)

            await member.add_roles(discord.utils.get(ctx.channel.guild.roles, id=roles[who][faculty]))
            await member.add_roles(discord.utils.get(ctx.channel.guild.roles, id=roles[who][who]))

    else:
        emb = discord.Embed(title="Эта команда не работает на этом сервере!", colour=discord.Colour.red())
        await ctx.send(embed=emb)