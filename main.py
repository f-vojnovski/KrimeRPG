from nextcord.ext import commands, tasks
import nextcord
import pymongo
from pymongo import MongoClient
import time
from datetime import datetime
from pytz import timezone
import traceback

from botdata import *
from util import *

# Top of Main.py

from webserver import keep_alive
import os

BOT_PREFIX = '$'
SUBSTANCES_CHANNEL_ID = 900828357996986388
BUSINESSES_CHANNEL_ID = 900828437005074452

# BOT SETUP
client = commands.Bot(command_prefix=BOT_PREFIX, case_insensitive=True)
client.remove_command('help')

# DATABASE SETUP
MONGO_CONN_STRING = os.environ['MONGO_CONN_STRING']

cluster = MongoClient(MONGO_CONN_STRING)
db = cluster['krime-bot']
user_collection = db['users']
drugs_collection = db['substances']
config_vars_collection = db['config_vars']
user_drug_collection = db['user_substance_storage']
user_gun_collection = db['user_gun_collection']
user_car_collection = db['user_car_collection']
business_collection = db['business_collection']


# BOT READY CHECK
@client.event
async def on_ready():
    print('Krime bot is ready!')

    change_drug_prices.start()
    cash_in_business.start()


@client.command(pass_context=True)
async def signup(ctx):
    try:
        post = {"_id": ctx.message.author.id, "health": max_health, "money": 0, "xp": 0, "heal_cd": 0, "jail_cd": 0,
                "crime_cd": 0, "death_cd": 0, "atk_cd": 0}
        user_collection.insert_one(post)

        await ctx.send(f"Добредојде во светот на криминалот, **{ctx.message.author.name}**. 👋🎉")
    except Exception as exc:
        await ctx.send(traceback.format_exc())


@client.command(name='stats')
async def show_user_stats(ctx):
    try:
        author_id = ctx.message.author.id
        author_name = ctx.message.author.name

        user_data = user_collection.find_one({'_id': author_id})

        if user_data is None:
            await ctx.send(f'Вие не сте најавени. За да почнете со играта напишете {BOT_PREFIX}signup.')
            return

        level = get_level_based_on_xp(user_data['xp'])

        await ctx.send(
            f"Статистика за **{author_name}:**\nЕнергија:**🩸{user_data['health']}**, Пари: **💵{user_data['money']}**, Ниво: **{level + 1}**, XP до следно ниво: **{get_xp_to_next_level(level, user_data['xp'])}**.")
    except Exception as exc:
        await ctx.send(traceback.format_exc())


@client.command(name='respawn')
async def respawn(ctx):
    try:
        author_id = ctx.message.author.id
        author_name = ctx.message.author.name

        user_data = user_collection.find_one({'_id': author_id})

        if user_data is None:
            await ctx.send(f'Вие не сте најавени. За да почнете со играта напишете {BOT_PREFIX}signup.')
            return

        curr_time = int(time.time())
        if user_data['death_cd'] >= curr_time:
            remaining_death_time = user_data['death_cd'] - curr_time
            await ctx.send(
                f"Треба да почекате уште **{get_formatted_min_secs(remaining_death_time)}** пред да respawn-ете.")
            return

        user_collection.update_one({'_id': author_id}, {"$set": {'death_cd': 0}}, upsert=False)
        user_collection.update_one({'_id': author_id}, {"$set": {'health': max_health}}, upsert=False)
        await ctx.send(f"**{author_name}** се врати во игра! 😊")
    except Exception as exc:
        await ctx.send(traceback.format_exc())


@client.command(name='crime')
async def commit_crime(ctx, arg):
    try:
        selected_crime = None

        for crime in crimes:
            if arg.lower() == crime['command'].lower():
                selected_crime = crime
                break

        if selected_crime is None:
            await ctx.send('Криминалното дело не е пронајдено на листата.')
            return

        player_name = ctx.message.author.name
        author_id = ctx.message.author.id

        user_data = user_collection.find_one({'_id': author_id})

        if user_data is None:
            await ctx.send(f'Вие не сте најавени. За да почнете со играта напишете {BOT_PREFIX}signup.')
            return

        curr_time = int(time.time())
        if user_data['death_cd'] != 0:
            remaining_death_time = user_data['death_cd'] - curr_time
            if user_data['death_cd'] >= curr_time:
                await ctx.send(
                    f"Вие сте мртви. Може да respawn-ете со **{BOT_PREFIX}respawn** за **{get_formatted_min_secs(remaining_death_time)}**.")
            else:
                await ctx.send(f"Вие сте мртви. Respawn-ете со **{BOT_PREFIX}respawn**.")
            return

        if user_data['jail_cd'] >= curr_time:
            remaining_jail_time = user_data['jail_cd'] - curr_time
            await ctx.send(
                f"Вие сте во затвор. Обидете се повторно за **{get_formatted_min_secs(remaining_jail_time)}**.")
            return

        if user_data['crime_cd'] >= curr_time:
            remaining_crime_cd = user_data['crime_cd'] - curr_time
            await ctx.send(
                f"Вие извршивте криминал скоро. Обидете се повторно за **{get_formatted_min_secs(remaining_crime_cd)}**.")
            return

        crime_cd = curr_time + selected_crime['crime_cd']
        user_collection.update_one({'_id': author_id}, {"$set": {'crime_cd': crime_cd}}, upsert=False)

        player_level = get_level_based_on_xp(user_data['xp'])
        crime_successful = check_event_based_on_probability(
            selected_crime['success_chance'] * levels[player_level]['crime_factor'])

        if crime_successful:
            money_gained = random.randint(selected_crime['min_profit'], selected_crime['max_profit'])
            xp_gained = random.randint(selected_crime['min_xp'], selected_crime['max_xp'])

            new_balance = user_data['money'] + money_gained
            user_collection.update_one({'_id': author_id}, {"$set": {'money': new_balance}}, upsert=False)

            new_xp = user_data['xp'] + xp_gained
            if new_xp >= levels[19]['xp']:
                new_xp = levels[19]['xp']

            user_collection.update_one({'_id': author_id}, {"$set": {'xp': new_xp}}, upsert=False)

            embed = nextcord.Embed(
                title=f'{player_name} успешно го изврши криминалното дело!',
                colour=nextcord.Colour.from_rgb(241, 196, 15)
            )

            embed.add_field(name='Заработени пари:', value=f"💵{money_gained}")
            embed.add_field(name='Добиено XP:', value=f"{xp_gained}")

            author_level = get_level_based_on_xp(user_data['xp'])
            new_level = get_level_based_on_xp(new_xp)
            if new_level != author_level:
                embed.add_field(name='Честитки!', value=f"{player_name} качи {new_level + 1} ниво.🎉🎈", inline=False)

            embed.set_image(url=random.choice(crime_successful_images))
            await ctx.send(embed=embed)
            return

        crime_escaped = check_event_based_on_probability(selected_crime['escape_chance'] * levels[player_level]['crime_factor'])

        if (crime_escaped):
            await ctx.send(
                f"**{player_name}** не успеа да го изврши криминалното дело 😢, но за среќа успеа да побегне од полицијата🚓.")
            return

        jail_time = random.randint(selected_crime['min_jail_time'], selected_crime['max_jail_time'])
        jail_cd = curr_time + jail_time
        user_collection.update_one({'_id': author_id}, {"$set": {'jail_cd': jail_cd}}, upsert=False)

        embed = nextcord.Embed(
            title=f'Полицијата🚓 го фати {player_name} и го однесе во затвор!😭😭😭',
            colour=nextcord.Colour.from_rgb(241, 196, 15)
        )

        embed.add_field(name='Изречена пресуда:', value=f"{jail_time} секунди во затвор.")

        embed.set_image(url=random.choice(crime_caught_images))
        await ctx.send(embed=embed)
    except:
        await ctx.send(await ctx.send(traceback.format_exc()))


@client.command(name='armedcrime')
async def commit_armed_crime(ctx, arg1, arg2):
    try:
        selected_crime = None

        for crime in armed_crimes:
            if arg1.lower() == crime['command'].lower():
                selected_crime = crime
                break

        if selected_crime is None:
            await ctx.send('Криминалното дело не е пронајдено на листата.')
            return

        selected_gun = None
        for gun in gun_data:
            if gun['name'] == arg2:
                selected_gun = gun
                break

        if selected_gun is None:
            await ctx.send('Оружјето не е пронајдено на листата.')
            return

        player_name = ctx.message.author.name
        author_id = ctx.message.author.id

        user_data = user_collection.find_one({'_id': author_id})

        if user_data is None:
            await ctx.send(f'Вие не сте најавени. За да почнете со играта напишете {BOT_PREFIX}signup.')
            return

        curr_time = int(time.time())
        if user_data['death_cd'] != 0:
            remaining_death_time = user_data['death_cd'] - curr_time
            if user_data['death_cd'] >= curr_time:
                await ctx.send(
                    f"Вие сте мртви. Може да respawn-ете со **{BOT_PREFIX}respawn** за **{get_formatted_min_secs(remaining_death_time)}**.")
            else:
                await ctx.send(f"Вие сте мртви. Respawn-ете со **{BOT_PREFIX}respawn**.")
            return

        if user_data['jail_cd'] >= curr_time:
            remaining_jail_time = user_data['jail_cd'] - curr_time
            await ctx.send(
                f"Вие сте во затвор. Обидете се повторно за **{get_formatted_min_secs(remaining_jail_time)}**.")
            return

        if user_data['crime_cd'] >= curr_time:
            remaining_crime_cd = user_data['crime_cd'] - curr_time
            await ctx.send(
                f"Вие извршивте криминал скоро. Обидете се повторно за **{get_formatted_min_secs(remaining_crime_cd)}**.")
            return

        user_guns = user_gun_collection.find_one({'_id': author_id})['value']

        user_gun_arr_index = -1
        for i in range(0, len(user_guns)):
            if user_guns[i] == selected_gun['id']:
                user_gun_arr_index = i
                break

        if user_gun_arr_index == -1:
            await ctx.send('Вие не го поседувате тоа оружје.')
            return

        crime_cd = curr_time + selected_crime['crime_cd']
        user_collection.update_one({'_id': author_id}, {"$set": {'crime_cd': crime_cd}}, upsert=False)

        player_level = get_level_based_on_xp(user_data['xp'])
        crime_successful = check_event_based_on_probability(
            selected_crime['success_chance'] * levels[player_level]['crime_factor'] * selected_gun['effectiveness'])

        if crime_successful:
            money_gained = random.randint(selected_crime['min_profit'], selected_crime['max_profit'])
            xp_gained = random.randint(selected_crime['min_xp'], selected_crime['max_xp'])

            new_balance = user_data['money'] + money_gained
            user_collection.update_one({'_id': author_id}, {"$set": {'money': new_balance}}, upsert=False)

            new_xp = user_data['xp'] + xp_gained
            if new_xp >= levels[19]['xp']:
                new_xp = levels[19]['xp']

            user_collection.update_one({'_id': author_id}, {"$set": {'xp': new_xp}}, upsert=False)

            embed = nextcord.Embed(
                title=f'{player_name} успешно го изврши криминалното дело!',
                colour=nextcord.Colour.from_rgb(241, 196, 15)
            )

            if check_event_based_on_probability(selected_gun['break_chance']):
                del [user_guns[user_gun_arr_index]]
                user_gun_collection.update_one({'_id': author_id}, {"$set": {'value': user_guns}})
                embed.add_field(name='Оружјето беше пронајдено од полцијата.',
                                value=f"{ctx.message.author.name} мораше да се ослободи од оружјето.", inline=False)

            embed.add_field(name='Заработени пари:', value=f"💵{money_gained}")
            embed.add_field(name='Добиено XP:', value=f"{xp_gained}")

            author_level = get_level_based_on_xp(user_data['xp'])
            new_level = get_level_based_on_xp(new_xp)
            if new_level != author_level:
                embed.add_field(name='Честитки!', value=f"{player_name} качи {new_level + 1} ниво.🎉🎈", inline=False)

            embed.set_image(url=random.choice(crime_successful_images))
            await ctx.send(embed=embed)
            return

        crime_escaped = check_event_based_on_probability(selected_crime['escape_chance'] * levels[player_level]['crime_factor'])

        if crime_escaped:
            await ctx.send(
                f"**{player_name}** не успеа да го изврши криминалното дело 😢, но за среќа успеа да побегне од полицијата🚓.")
            return

        jail_time = random.randint(selected_crime['min_jail_time'], selected_crime['max_jail_time'])
        jail_cd = curr_time + jail_time
        user_collection.update_one({'_id': author_id}, {"$set": {'jail_cd': jail_cd}}, upsert=False)

        embed = nextcord.Embed(
            title=f'Полицијата🚓 го фати {player_name} и го однесе во затвор!😭😭😭',
            colour=nextcord.Colour.from_rgb(241, 196, 15)
        )

        del [user_guns[user_gun_arr_index]]
        user_gun_collection.update_one({'_id': author_id}, {"$set": {'value': user_guns}})

        embed.add_field(name='Изречена пресуда:', value=f"{jail_time} секунди во затвор.")

        embed.set_image(url=random.choice(crime_caught_images))
        await ctx.send(embed=embed)
    except Exception as exc:
        await ctx.send(traceback.format_exc())


@client.command(name='buydrugs', pass_context=True)
async def buy_drugs(ctx, arg1, arg2):
    try:
        try:
            int(arg2)
        except ValueError:
            await ctx.send('Внесена невалидна количина!')
            return

        buying_amount = int(arg2)

        if buying_amount <= 0:
            await ctx.send('Внесена невалидна количина!')
            return

        author_id = ctx.message.author.id
        author_name = ctx.message.author.name

        selected_drug = None

        for drug in substances_data:
            if drug['name'] == arg1:
                selected_drug = drug

        if selected_drug is None:
            await ctx.send(
                f'Дадената супстанција не е пронајдена на црниот пазар. За листа на супстанции погледнете го туторијалот.')
            return

        user_data = user_collection.find_one({"_id": author_id})

        curr_time = int(time.time())
        if user_data['death_cd'] != 0:
            remaining_death_time = user_data['death_cd'] - curr_time
            if user_data['death_cd'] >= curr_time:
                await ctx.send(
                    f"Вие сте мртви. Може да respawn-ете со **{BOT_PREFIX}respawn** за **{get_formatted_min_secs(remaining_death_time)}**.")
            else:
                await ctx.send(f"Вие сте мртви. Respawn-ете со **{BOT_PREFIX}respawn**.")
            return

        if user_data['jail_cd'] >= curr_time:
            remaining_jail_time = user_data['jail_cd'] - curr_time
            await ctx.send(
                f"Вие сте во затвор. Обидете се повторно за **{get_formatted_min_secs(remaining_jail_time)}**.")
            return

        drug_user_storage = user_drug_collection.find_one({"_id": f"{author_id} {selected_drug['id']}"})

        drug_in_database = drugs_collection.find_one({"_id": selected_drug['id']})
        drug_price = drug_in_database['price'] * buying_amount

        if user_data['money'] < drug_price:
            await ctx.send('Немате доволно пари.')
            return

        if drug_user_storage is None:
            new_amount = buying_amount
            if new_amount > selected_drug['max_amount']:
                await ctx.send(f"Може да купите максимум {selected_drug['max_amount']}kg {selected_drug['name']}.")
                return

            user_drug_collection.insert_one(
                {'_id': f"{author_id} {selected_drug['id']}", 'user': author_id, 'amount': new_amount})
        else:
            curr_amount = int(drug_user_storage['amount'])
            new_amount = curr_amount + buying_amount
            if new_amount > selected_drug['max_amount']:
                await ctx.send(
                    f"Може да поседувате максимум {selected_drug['max_amount']}kg {selected_drug['name']} во даден момент. Максимум количина која што може да ја купите од оваа супстанца: {selected_drug['max_amount'] - curr_amount}kg.")
                return
            user_drug_collection.update_one({'_id': f"{author_id} {selected_drug['id']}"},
                                            {"$set": {'amount': new_amount}},
                                            upsert=False)

        new_balance = user_data['money'] - drug_price
        user_collection.update_one({'_id': author_id}, {"$set": {'money': new_balance}}, upsert=False)
        await ctx.send(f'**{author_name}** купи {buying_amount}kg {arg1}.')
    except Exception as exc:
        await ctx.send(traceback.format_exc())


@client.command(name='selldrugs', pass_context=True)
async def sell_drugs(ctx, arg1, arg2):
    try:
        try:
            int(arg2)
        except ValueError:
            await ctx.send('Внесена невалидна количина!')
            return

        selling_amount = int(arg2)

        if selling_amount <= 0:
            await ctx.send('Внесена невалидна количина!')
            return

        author_id = ctx.message.author.id
        author_name = ctx.message.author.name

        selected_drug = None

        for drug in substances_data:
            if drug['name'] == arg1:
                selected_drug = drug

        if selected_drug is None:
            await ctx.send('Дадената супстанција не е пронајдена во вашиот магацин.')
            return

        user_data = user_collection.find_one({"_id": author_id})

        curr_time = int(time.time())
        if user_data['death_cd'] != 0:
            remaining_death_time = user_data['death_cd'] - curr_time
            if user_data['death_cd'] >= curr_time:
                await ctx.send(
                    f"Вие сте мртви. Може да respawn-ете со **{BOT_PREFIX}respawn** за **{get_formatted_min_secs(remaining_death_time)}**.")
            else:
                await ctx.send(f"Вие сте мртви. Respawn-ете со **{BOT_PREFIX}respawn**.")
            return

        if user_data['jail_cd'] >= curr_time:
            remaining_jail_time = user_data['jail_cd'] - curr_time
            await ctx.send(
                f"Вие сте во затвор. Обидете се повторно за **{get_formatted_min_secs(remaining_jail_time)}**.")
            return

        drug_user_storage = user_drug_collection.find_one({"_id": f"{author_id} {selected_drug['id']}"})

        if drug_user_storage is None:
            await ctx.send('Ја немате оваа роба во вашиот магацин.')
            return

        if drug_user_storage['amount'] < selling_amount:
            await ctx.send('Немате толкава количина во вашиот магацин.')
            return

        police_activity = config_vars_collection.find_one({"_id": 1})['value']

        if check_event_based_on_probability(police_activity):
            if police_activity < drug_dealing_police_dont_arrest or check_event_based_on_probability(
                    police_activity * drug_dealing_escape_chance_multiplier, opposite=True):
                await ctx.send(
                    f"За време на зделката се појави полиција🚓. За среќа, **{author_name}** успеа да избега со робата📦.")
                return

            new_amount = int(drug_user_storage['amount']) - selling_amount

            user_drug_collection.update_one({'_id': f"{author_id} {selected_drug['id']}"},
                                            {"$set": {'amount': new_amount}},
                                            upsert=False)

            embed = nextcord.Embed(
                title=f"Полицијата🚓 знаеше за зделката🤝. **{author_name}** беше уапцен, а робата📦 му беше запленета.😭😭😭",
                colour=nextcord.Colour.from_rgb(241, 196, 15)
            )

            jail_time = random.randint(drug_dealing_jail['min_time'], drug_dealing_jail['max_time'])
            jail_cd = curr_time + jail_time
            user_collection.update_one({'_id': author_id}, {"$set": {'jail_cd': jail_cd}}, upsert=False)

            embed.add_field(name='Изречена пресуда:', value=f"{jail_time} секунди во затвор.")

            embed.set_image(url=random.choice(crime_caught_images))
            await ctx.send(embed=embed)
            return

        new_amount = int(drug_user_storage['amount']) - selling_amount
        user_drug_collection.update_one({'_id': f"{author_id} {selected_drug['id']}"}, {"$set": {'amount': new_amount}},
                                        upsert=False)

        drug_in_database = drugs_collection.find_one({"_id": selected_drug['id']})
        drug_price = drug_in_database['price'] * selling_amount
        new_balance = user_data['money'] + drug_price
        user_collection.update_one({'_id': author_id}, {"$set": {'money': new_balance}}, upsert=False)

        embed = nextcord.Embed(
            title=f"{author_name} успешно изврши продажба на {selected_drug['name']}!",
            colour=nextcord.Colour.from_rgb(241, 196, 15)
        )

        embed.add_field(name='Заработка:', value=f"💵{drug_price}")
        embed.set_image(url=random.choice(drug_deal_successful_images))
        await ctx.send(embed=embed)

    except Exception as exc:
        await ctx.send(traceback.format_exc())


@client.command(name='mydrugs')
async def user_list_drugs(ctx):
    try:
        author_id = ctx.message.author.id
        user_drugs = user_drug_collection.find({"user": author_id})

        user_drugs_str = 'Во вашиот магацин имате:\n```'

        for drug in user_drugs:
            if drug['amount'] <= 0: continue
            drug_id = int(drug['_id'].split()[1])
            drug_name = substances_data[drug_id - 1]['name']
            user_drugs_str += f"{drug_name}: {drug['amount']}kg\n"

        user_drugs_str += '```'

        await ctx.send(user_drugs_str)
    except Exception as exc:
        await ctx.send(traceback.format_exc())


@tasks.loop(seconds=drug_market_price_change_period)
async def change_drug_prices():
    try:
        channel = client.get_channel(SUBSTANCES_CHANNEL_ID)

        embed = nextcord.Embed(
            title="Промени на цените на недозволени супстанции на црниот пазар",
            colour=nextcord.Colour.from_rgb(241, 196, 15)
        )

        drug_list = drugs_collection.find({})
        for document in drug_list:
            substance = substances_data[document['_id'] - 1]
            current_drug_price = document['price']
            old_drug_price = current_drug_price
            price_change = random.randint(substance['min_price_change'], substance['max_price_change'])

            increase_probability = (
                    (substance['max_price'] - current_drug_price) / (substance['max_price'] - substance['min_price']))

            if current_drug_price <= substance['max_price'] and (
                    check_event_based_on_probability(increase_probability) or current_drug_price <= substance[
                'min_price']):
                current_drug_price += price_change
                current_drug_price = clamp_int(current_drug_price, substance['min_price'],
                                               substance['max_price']) + random.randint(1, drug_price_magic_number)
                drugs_collection.update_one({'_id': document['_id']}, {"$set": {'price': current_drug_price}},
                                            upsert=False)
                embed.add_field(name=f"Поскапување на {substance['name']}",
                                value=f"💵{old_drug_price}/kg => 💵{current_drug_price}/kg", inline=False)
            else:
                current_drug_price -= price_change
                current_drug_price = clamp_int(current_drug_price, substance['min_price'],
                                               substance['max_price']) - random.randint(1, drug_price_magic_number)
                drugs_collection.update_one({'_id': document['_id']}, {"$set": {'price': current_drug_price}},
                                            upsert=False)
                embed.add_field(name=f"Поевтинување на {substance['name']}",
                                value=f"💵{old_drug_price}/kg => 💵{current_drug_price}/kg", inline=False)

        police_activity = random.uniform(police_activity_range['min_activity'], police_activity_range['max_activity'])

        config_vars_collection.update_one({'_id': 1}, {"$set": {'value': police_activity}}, upsert=False)
        embed.set_footer(text=f'Шпионите од полицијата велат: {get_police_activity_string(police_activity)}')

        await channel.send(embed=embed)
    except Exception as exc:
        pass


@client.command(name="buygun")
async def buy_gun(ctx, arg1):
    try:
        selected_gun = None
        for gun in gun_data:
            if arg1 == gun['name']:
                selected_gun = gun
                break

        if selected_gun is None:
            await ctx.send('Даденото оружје не е пронајдено на листата.')
            return

        author_id = ctx.message.author.id
        user_data = user_collection.find_one({"_id": author_id})

        curr_time = int(time.time())
        if user_data['death_cd'] != 0:
            remaining_death_time = user_data['death_cd'] - curr_time
            if user_data['death_cd'] >= curr_time:
                await ctx.send(
                    f"Вие сте мртви. Може да respawn-ете со **{BOT_PREFIX}respawn** за **{get_formatted_min_secs(remaining_death_time)}**.")
            else:
                await ctx.send(f"Вие сте мртви. Respawn-ете со **{BOT_PREFIX}respawn**.")
            return

        if user_data['jail_cd'] >= curr_time:
            remaining_jail_time = user_data['jail_cd'] - curr_time
            await ctx.send(
                f"Вие сте во затвор. Обидете се повторно за **{get_formatted_min_secs(remaining_jail_time)}**")
            return

        if user_data['money'] < selected_gun['price']:
            await ctx.send('Немате доволно пари.')
            return

        new_balance = user_data['money'] - selected_gun['price']
        user_collection.update_one({'_id': author_id}, {"$set": {'money': new_balance}}, upsert=False)

        user_gun_data = user_gun_collection.find_one({"_id": author_id})
        if user_gun_data is None:
            user_gun_collection.insert_one({'_id': author_id, "value": [selected_gun['id']]})
        else:
            user_gun_list = user_gun_data['value']
            if len(user_gun_list) > gun_storage_limit:
                await ctx.send(f"Вие веќе имате {gun_storage_limit} оружја. Не може да купете повеќе.")
                return
            user_gun_list.append(selected_gun['id'])
            user_gun_collection.update_one({'_id': author_id}, {"$set": {'value': user_gun_list}}, upsert=False)

        author_name = ctx.message.author.name
        await ctx.send(f"**{author_name}** купи {selected_gun['name']}.")
    except Exception as exc:
        await ctx.send(traceback.format_exc())


@client.command(name='sellgun')
async def user_sell_gun(ctx, arg1):
    try:
        author_id = ctx.message.author.id
        selected_gun = None
        for gun in gun_data:
            if gun['name'] == arg1:
                selected_gun = gun
                break

        if selected_gun is None:
            await ctx.send('Не постои такво оружје во играта.')
            return

        user_guns = user_gun_collection.find_one({'_id': author_id})['value']
        if user_guns is None:
            await ctx.send('Вие немате оружје.')
            return

        user_data = user_collection.find_one({"_id": author_id})

        curr_time = int(time.time())
        if user_data['death_cd'] != 0:
            remaining_death_time = user_data['death_cd'] - curr_time
            if user_data['death_cd'] >= curr_time:
                await ctx.send(
                    f"Вие сте мртви. Може да respawn-ете со **{BOT_PREFIX}respawn** за **{get_formatted_min_secs(remaining_death_time)}**.")
            else:
                await ctx.send(f"Вие сте мртви. Respawn-ете со **{BOT_PREFIX}respawn**.")
            return

        if user_data['jail_cd'] >= curr_time:
            remaining_jail_time = user_data['jail_cd'] - curr_time
            await ctx.send(
                f"Вие сте во затвор. Обидете се повторно за **{get_formatted_min_secs(remaining_jail_time)}**")
            return

        for i in range(0, len(user_guns)):
            if user_guns[i] == selected_gun['id']:
                money_gained = int(selected_gun['price'] * gun_sell_price_penalty)

                new_balance = user_data['money'] + money_gained
                user_collection.update_one({'_id': author_id}, {"$set": {'money': new_balance}}, upsert=False)

                del [user_guns[i]]
                user_gun_collection.update_one({'_id': author_id}, {"$set": {'value': user_guns}})

                await ctx.send(f"**{ctx.message.author.name}** продаде {selected_gun['name']} за 💵{money_gained}.")
                return

        await ctx.send('Вие не поседувате такво оружје.')
    except Exception as exc:
        await ctx.send(traceback.format_exc())


@client.command(name="myguns")
async def user_list_guns(ctx):
    try:
        author_id = ctx.message.author.id
        user_guns = user_gun_collection.find_one({'_id': author_id})

        if len(user_guns['value']) == 0:
            await ctx.send(f"{ctx.message.author.name} не поседува оружје.")
            return

        user_gun_list_str = '`'
        for gun in user_guns['value']:
            gun_name = gun_data[gun]['name']
            user_gun_list_str += f"{gun_name}, "

        user_gun_list_str = user_gun_list_str[:-2]
        user_gun_list_str += '`'
        await ctx.send(f"**{ctx.message.author.name}** поседува: {user_gun_list_str}")
    except Exception as exc:
        await ctx.send(traceback.format_exc())


@client.command(name="attack")
async def attack_player(ctx, arg1):
    try:
        eusk = timezone('Europe/Skopje')
        sk_time = datetime.now(eusk)
        hour = int(sk_time.strftime('%H'))
        if 1 <= hour < 17:
            await ctx.send('Напаѓање е возможно само од 17:00 до 01:00 часот секој ден.')
            return

        attacked_user_id = ctx.message.mentions[0].id

        selected_gun = None
        for gun in gun_data:
            if gun['name'] == arg1:
                selected_gun = gun
                break

        if selected_gun is None:
            await ctx.send('Оружјето не е пронајдено на листата.')
            return

        if attacked_user_id is None:
            await ctx.send('Играчот не е пронајден.')
            return

        author_id = ctx.message.author.id
        if attacked_user_id == author_id:
            await ctx.send('Не можеш да се нападнеш самиот себе.')
            return

        user_attacking = user_collection.find_one({'_id': author_id})

        curr_time = int(time.time())
        if user_attacking['death_cd'] != 0:
            remaining_death_time = user_attacking['death_cd'] - curr_time
            if user_attacking['death_cd'] >= curr_time:
                await ctx.send(
                    f"Вие сте мртви. Може да respawn-ете со **{BOT_PREFIX}respawn** за **{get_formatted_min_secs(remaining_death_time)}**.")
            else:
                await ctx.send(f"Вие сте мртви. Respawn-ете со **{BOT_PREFIX}respawn**.")
            return

        if user_attacking['jail_cd'] >= curr_time:
            remaining_jail_time = user_attacking['jail_cd'] - curr_time
            await ctx.send(
                f"Вие сте во затвор. Обидете се повторно за **{get_formatted_min_secs(remaining_jail_time)}**.")
            return

        if user_attacking['atk_cd'] >= curr_time:
            remaining_atk_time = user_attacking['atk_cd'] - curr_time
            await ctx.send(
                f"Вие нападнавте пред малку. Обидете се повторно за **{get_formatted_min_secs(remaining_atk_time)}**.")
            return

        user_guns = user_gun_collection.find_one({'_id': author_id})['value']

        user_gun_arr_index = -1
        for i in range(0, len(user_guns)):
            if user_guns[i] == selected_gun['id']:
                user_gun_arr_index = i
                break

        if user_gun_arr_index == -1:
            await ctx.send('Вие не го поседувате тоа оружје.')
            return

        attacked_user = user_collection.find_one({'_id': attacked_user_id})

        user_attacking_level = get_level_based_on_xp(user_attacking['xp'])

        if user_attacking_level < attack_level_requirement:
            await ctx.send(f"За напаѓање е потребно {attack_level_requirement + 1}-то ниво.")
            return

        if attacked_user is None:
            await ctx.send('Овој корисник засега не ја игра играта.')
            return

        if attacked_user['death_cd'] != 0:
            await ctx.send('Овој корисник е веќе мртов.')
            return

        gun_damage = int(
            random.randint(selected_gun['min_damage'],
                           selected_gun['max_damage']) * get_damage_multiplier_based_on_level(
                user_attacking_level))
        gun_damage += base_attack_damage
        attacked_user_health = attacked_user['health'] - gun_damage

        user_collection.update_one({'_id': attacked_user_id}, {"$set": {'health': attacked_user_health}})
        user_attack_cooldown = curr_time + attack_cooldown
        user_collection.update_one({'_id': author_id}, {"$set": {'atk_cd': user_attack_cooldown}})

        if attacked_user_health <= 0:
            embed = nextcord.Embed(
                title=f"{ctx.message.mentions[0].name} беше убиен од страна на {ctx.message.author.name}",
                colour=nextcord.Colour.from_rgb(241, 196, 15)
            )

            xp_gained = (get_level_based_on_xp(attacked_user['xp']) + 1) * killed_user_xp_multiplier
            new_xp = user_attacking['xp'] + xp_gained
            if new_xp >= levels[19]['xp']:
                new_xp = levels[19]['xp']

            money_gained = int(kill_money_gain_ratio * attacked_user['money']) + kill_min_money
            money_lost = int(death_money_loss_ratio * attacked_user['money'])
            new_balance_attacker = user_attacking['money'] + money_gained
            new_balance_attacked = attacked_user['money'] - money_lost

            user_collection.update_one({'_id': author_id}, {"$set": {'money': new_balance_attacker}})
            user_collection.update_one({'_id': attacked_user_id}, {"$set": {'money': new_balance_attacked}})
            embed.add_field(name='Добиено xp и пари:', value=f"+{xp_gained}xp, 💵{money_gained}", inline=False)

            new_level = get_level_based_on_xp(new_xp)
            if new_level != user_attacking_level:
                embed.add_field(name='Честитки!', value=f"{ctx.message.author.name} качи {new_level + 1} ниво.🎉🎈",
                                inline=False)

            user_collection.update_one({'_id': author_id}, {"$set": {'xp': new_xp}})

            user_death_cd = curr_time + death_cooldown
            user_collection.update_one({'_id': attacked_user_id}, {"$set": {'death_cd': user_death_cd}}, upsert=False)

            businesses = list(business_collection.find({"owner": {"$eq": attacked_user_id}}))

            if len(businesses) > 0:
                lost_businesses_str = ''

                for business_db in businesses:
                    business_collection.update_one({'_id': business_db['_id']}, {"$set": {'owner': 0}})
                    lost_businesses_str += f"{businessdata.businesses_data[business_db['_id']]['name']}, "

                lost_businesses_str = lost_businesses_str[:-2]
                embed.add_field(name='Изгубени бизниси:', value=lost_businesses_str, inline=False)
                business_channel = client.get_channel(BUSINESSES_CHANNEL_ID)
                await business_channel.send(f"Бизнисите: {lost_businesses_str} се сега достапни за купување")

            user_collection.update_one({'_id': attacked_user_id}, {"$set": {'death_cd': curr_time + death_cooldown}})

            embed.set_image(url=random.choice(user_killed_images))

            if check_event_based_on_probability(selected_gun['break_chance']):
                del [user_guns[user_gun_arr_index]]
                user_gun_collection.update_one({'_id': author_id}, {"$set": {'value': user_guns}})
                embed.add_field(name='Оружјето беше пронајдено од полицијата.',
                                value=f"{ctx.message.author.name} мораше да се ослободи од оружјето.", inline=False)

            await ctx.send(embed=embed)
            return

        embed = nextcord.Embed(
            title=f"{ctx.message.author.name} го нападна {ctx.message.mentions[0].name}",
            colour=nextcord.Colour.from_rgb(241, 196, 15)
        )

        xp_gained = (get_level_based_on_xp(attacked_user['xp']) * attack_user_xp_multiplier) + attacking_min_xp
        new_xp = user_attacking['xp'] + xp_gained
        if new_xp >= levels[19]['xp']:
            new_xp = levels[19]['xp']

        money_gained = int(attack_money_gain_ratio * attacked_user['money']) + attacking_min_money
        money_lost = int(attacked_money_loss_ratio * attacked_user['money'])
        new_balance_attacker = user_attacking['money'] + money_gained
        new_balance_attacked = attacked_user['money'] - money_lost

        user_collection.update_one({'_id': author_id}, {"$set": {'money': new_balance_attacker}})
        user_collection.update_one({'_id': attacked_user_id}, {"$set": {'money': new_balance_attacked}})
        embed.add_field(name='Добиено xp и пари:', value=f"+{xp_gained}xp, 💵{money_gained}", inline=False)

        new_level = get_level_based_on_xp(new_xp)
        if new_level != user_attacking_level:
            embed.add_field(name='Честитки!', value=f"{ctx.message.author.name} качи {new_level + 1} ниво.🎉🎈",
                            inline=False)

        user_collection.update_one({'_id': author_id}, {"$set": {'xp': new_xp}})

        if check_event_based_on_probability(selected_gun['break_chance']):
            del [user_guns[user_gun_arr_index]]
            user_gun_collection.update_one({'_id': author_id}, {"$set": {'value': user_guns}})
            embed.add_field(name='Оружјето беше пронајдено од полицијата.',
                            value=f"{ctx.message.author.name} мораше да се ослободи од оружјето.", inline=False)

        embed.add_field(name='Направена штета:', value=f"{gun_damage}")
        embed.add_field(name='Нападнатиот е сега на:', value=f"{attacked_user_health}hp")

        embed.set_image(url=random.choice(attack_user_images))
        await ctx.send(embed=embed)
    except Exception as exc:
        await ctx.send(traceback.format_exc())


@client.command(name='heal')
async def heal(ctx):
    try:
        author_id = ctx.message.author.id
        author_name = ctx.message.author.name

        user_data = user_collection.find_one({'_id': author_id})

        if user_data is None:
            await ctx.send(f'Вие не сте најавени. За да почнете со играта напишете {BOT_PREFIX}signup.')
            return

        curr_time = int(time.time())
        if user_data['death_cd'] != 0:
            remaining_death_time = user_data['death_cd'] - curr_time
            if user_data['death_cd'] >= curr_time:
                await ctx.send(
                    f"Вие сте мртви. Може да respawn-ете со **{BOT_PREFIX}respawn** за **{get_formatted_min_secs(remaining_death_time)}**.")
            else:
                await ctx.send(f"Вие сте мртви. Respawn-ете со **{BOT_PREFIX}respawn**.")
            return

        if user_data['health'] == max_health:
            await ctx.send(f'Вие сте на full hp. Немате потреба од лечење.')
            return

        curr_time = int(time.time())
        if user_data['jail_cd'] >= curr_time:
            remaining_jail_time = user_data['jail_cd'] - curr_time
            await ctx.send(
                f"Вие сте во затвор. Обидете се повторно за **{get_formatted_min_secs(remaining_jail_time)}**")
            return

        if curr_time <= user_data['heal_cd']:
            time_remaining = (curr_time - user_data['heal_cd']) * -1
            await ctx.send(
                f"Вие бевте во болница скоро. Обидете се повторно за **{get_formatted_min_secs(time_remaining)}.**")
            return

        user_health = user_data['health'] + heal_amount
        new_health = clamp_int(user_health, 0, max_health)
        new_balance = int(user_data['money'] * heal_price_factor)

        heal_cd = curr_time + heal_cooldown

        user_collection.update_one({'_id': author_id}, {"$set": {'health': new_health}}, upsert=False)
        user_collection.update_one({'_id': author_id}, {"$set": {'money': new_balance}}, upsert=False)
        user_collection.update_one({'_id': author_id}, {"$set": {'heal_cd': heal_cd}})

        await ctx.send(
            f"**{author_name}** беше во болница. Сега е на **🩸{new_health}** hp, а медицинските трошоци коштаа **💵{int(user_data['money'] * (1 - heal_price_factor))}**.")
    except Exception as exc:
        await ctx.send(traceback.format_exc())


@client.command(name='buybusiness')
async def buy_business(ctx, arg):
    try:
        author_id = ctx.message.author.id
        author_name = ctx.message.author.name

        selected_business = None
        for business in businessdata.businesses_data:
            if business['command'] == arg:
                selected_business = business
                break

        if selected_business is None:
            await ctx.send("Не постои таков бизнис. Проверете ја листата.")
            return

        user_data = user_collection.find_one({'_id': author_id})

        if user_data is None:
            await ctx.send(f'Вие не сте најавени. За да почнете со играта напишете {BOT_PREFIX}signup.')
            return

        curr_time = int(time.time())
        if user_data['death_cd'] != 0:
            remaining_death_time = user_data['death_cd'] - curr_time
            if user_data['death_cd'] >= curr_time:
                await ctx.send(
                    f"Вие сте мртви. Може да respawn-ете со **{BOT_PREFIX}respawn** за **{get_formatted_min_secs(remaining_death_time)}**.")
            else:
                await ctx.send(f"Вие сте мртви. Respawn-ете со **{BOT_PREFIX}respawn**.")
            return

        if user_data['jail_cd'] >= curr_time:
            remaining_jail_time = user_data['jail_cd'] - curr_time
            await ctx.send(
                f"Вие сте во затвор. Обидете се повторно за **{get_formatted_min_secs(remaining_jail_time)}**")
            return

        if user_data['money'] <= selected_business['price']:
            await ctx.send(
                f"Вие немате доволно пари за да го купите овој бизнис. Вие имате: **💵{user_data['money']}**. Потребни се: **${selected_business['price']}**")
            return

        bussines_in_data = business_collection.find_one({"_id": selected_business['id']})
        if bussines_in_data['owner'] != 0:
            await ctx.send(
                "Овој бизнис веќе има сопственик. За овој бизнис повторно да биде достапен за купување, сопственикот мора да биде ликвидиран.")
            return

        new_balance = int(user_data['money'] - selected_business['price'])
        user_collection.update_one({"_id": author_id}, {"$set": {'money': new_balance}}, upsert=False)
        business_collection.update_one({"_id": selected_business['id']}, {"$set": {'owner': author_id}}, upsert=False)

        business_str = f"**{author_name}** го купи бизнисот **{selected_business['name']}** за **💵{selected_business['price']}**."
        await ctx.send(business_str)
        channel = client.get_channel(BUSINESSES_CHANNEL_ID)
        await channel.send(business_str)
    except Exception as exc:
        await ctx.send(traceback.format_exc())


@tasks.loop(seconds=7203)
async def cash_in_business():
    try:
        businesses_in_db = business_collection.find({"owner": {"$ne": 0}})
        businesses_str = '**Пари заработени од бизниси**\n'
        channel = client.get_channel(BUSINESSES_CHANNEL_ID)
        await channel.send(businesses_str)

        for business_db in businesses_in_db:
            username = await client.fetch_user(business_db['owner'])
            curr_business = businessdata.businesses_data[business_db['_id']]
            money_earned = random.randint(curr_business['min_profit'], curr_business['max_profit'])
            businesses_str = f"{curr_business['name']}, **{username}** заработи **💵{money_earned}**.\n"
            user_data = user_collection.find_one({"_id": business_db['owner']})
            new_balance = user_data['money'] + money_earned
            user_collection.update_one({'_id': business_db['owner']}, {"$set": {'money': new_balance}}, upsert=False)
            await channel.send(businesses_str)

    except Exception as exc:
        pass


TOKEN = os.environ['BOT_TOKEN']
keep_alive()
client.run(TOKEN)
