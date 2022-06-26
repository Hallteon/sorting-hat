import discord

channel_roles = [
    "gryffindor - ученик",
    "slytherin - ученик",
    "hufflepuff - ученик",
    "ravenclaw - ученик",
    "death eaters - ученик",
    "gryffindor - наставник",
    "slytherin - наставник",
    "hufflepuff - наставник",
    "ravenclaw - наставник",
    "death eaters - наставник",
    "ждущие зачисления",
    "ученик",
    "наставник",
]

names_faculties = {
    "gryff": "Гриффиндор",
    "slyth": "Слизерин",
    "huff": "Пуффендуй",
    "raven": "Когтевран",
    "death": "Пожиратели Смерти"
}

start_emb = discord.Embed(title="Приветствую тебя, маг!", colour=discord.Colour.orange(),
                          description="Выбери вариант распределения:")

who_emb = discord.Embed(title="Для начала выбери кто ты:", colour=discord.Colour.purple())

select_fac_emb = discord.Embed(title="Выбери факультет:", colour=discord.Colour.red(),
                               description="Выбери понравившийся тебе факультет.")

question1_emb = discord.Embed(title="Давай пройдём небольшой тест.", colour=discord.Colour.green(),
                              description="Первый вопрос - какой ты?:")

question2_emb = discord.Embed(title="Второй вопрос:", colour=discord.Colour.orange(),
                              description="Какое животное тебе нравится больше всего?")

question3_emb = discord.Embed(title="Третий вопрос:", colour=discord.Colour.purple(),
                              description="Какая стихия нравится тебе больше всего?")

question4_emb = discord.Embed(title="Четвёртый вопрос:", colour=discord.Colour.blue(),
                              description="Какие комбинации цветов нравятся тебе больше всего?")

question5_emb = discord.Embed(title="Пятый вопрос:", colour=discord.Colour.red(),
                              description="Какое привидение из Хогвартса нравится тебе больше всего?")