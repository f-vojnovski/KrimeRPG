import businessdata

max_health = 1000
heal_amount = 300
heal_price_factor = 0.91
heal_cooldown = 3600
base_attack_damage = 27

attacking_min_money = 12000
attacking_min_xp = 700
kill_min_money = 25000

crimes = [
    {
        "name": "Крадење новчаник",
        "command": "pickpocket",
        "success_chance": 0.83,
        "escape_chance": 0.9,
        "min_profit": 50,
        "max_profit": 100,
        "min_jail_time": 16,
        "max_jail_time": 21,
        "min_xp": 55,
        "max_xp": 95,
        "crime_cd": 10
    },
    {
        "name": "Измама со кредитни картички",
        "command": "creditcardscam",
        "success_chance": 0.75,
        "escape_chance": 0.85,
        "min_profit": 70,
        "max_profit": 200,
        "min_jail_time": 16,
        "max_jail_time": 26,
        "min_xp": 60,
        "max_xp": 110,
        "crime_cd": 13
    },
    {
        "name": "Кражба на трафика",
        "command": "shoplift",
        "success_chance": 0.64,
        "escape_chance": 0.82,
        "min_profit": 150,
        "max_profit": 300,
        "min_jail_time": 21,
        "max_jail_time": 36,
        "min_xp": 120,
        "max_xp": 160,
        "crime_cd": 16
    },
    {
        "name": "Кражба од паркирано возило",
        "command": "cartheft",
        "success_chance": 0.52,
        "escape_chance": 0.7,
        "min_profit": 300,
        "max_profit": 550,
        "min_jail_time": 27,
        "max_jail_time": 44,
        "min_xp": 150,
        "max_xp": 230,
        "crime_cd": 24
    },
    {
        "name": "Кражба на банкомат",
        "command": "atmtheft",
        "success_chance": 0.31,
        "escape_chance": 0.38,
        "min_profit": 500,
        "max_profit": 1000,
        "min_jail_time": 37,
        "max_jail_time": 54,
        "min_xp": 150,
        "max_xp": 380,
        "crime_cd": 29
    }
]

armed_crimes = [
    {
        "name": "Упад во куќа",
        "command": "homeinvasion",
        "success_chance": 0.23,
        "escape_chance": 0.4,
        "min_profit": 4000,
        "max_profit": 7500,
        "min_jail_time": 40,
        "max_jail_time": 70,
        "min_xp": 250,
        "max_xp": 450,
        "crime_cd": 28
    },
    {
        "name": "Грабеж на супермаркет",
        "command": "marketrobbery",
        "success_chance": 0.21,
        "escape_chance": 0.37,
        "min_profit": 4400,
        "max_profit": 6200,
        "min_jail_time": 40,
        "max_jail_time": 70,
        "min_xp": 300,
        "max_xp": 500,
        "crime_cd": 33
    },
    {
        "name": "Кражба на магацин",
        "command": "warehouserobbery",
        "success_chance": 0.18,
        "escape_chance": 0.3,
        "min_profit": 5500,
        "max_profit": 9000,
        "min_jail_time": 70,
        "max_jail_time": 110,
        "min_xp": 500,
        "max_xp": 800,
        "crime_cd": 43
    },
    {
        "name": "Кражба на накит",
        "command": "jewelrytheft",
        "success_chance": 0.12,
        "escape_chance": 0.25,
        "min_profit": 9000,
        "max_profit": 17000,
        "min_jail_time": 80,
        "max_jail_time": 120,
        "min_xp": 1200,
        "max_xp": 2000,
        "crime_cd": 63
    },
    {
        "name": "Киднапирање на важна личност",
        "command": "kidnapping",
        "success_chance": 0.069,
        "escape_chance": 0.17,
        "min_profit": 19000,
        "max_profit": 27600,
        "min_jail_time": 90,
        "max_jail_time": 140,
        "min_xp": 1200,
        "max_xp": 2300,
        "crime_cd": 78
    },
    {
        "name": "Шверцување преку граница",
        "command": "trafficking",
        "success_chance": 0.05,
        "escape_chance": 0.15,
        "min_profit": 28000,
        "max_profit": 60000,
        "min_jail_time": 115,
        "max_jail_time": 155,
        "min_xp": 1900,
        "max_xp": 3000,
        "crime_cd": 93
    },
    {
        "name": "Грабеж на банка",
        "command": "bankheist",
        "success_chance": 0.02,
        "escape_chance": 0.1,
        "min_profit": 300000,
        "max_profit": 700000,
        "min_jail_time": 145,
        "max_jail_time": 205,
        "min_xp": 3000,
        "max_xp": 4000,
        "crime_cd": 123
    },
]

crime_successful_images = [
    'https://i.imgur.com/nGuUNE5.png',
    'https://i.imgur.com/RER0V0C.png',
    'https://i.imgur.com/fzDnxW7.png',
    'https://i.imgur.com/3HVks4s.png',
    'https://i.imgur.com/4qyt2XQ.png',
    'https://i.imgur.com/Oz9He6O.png',
    'https://i.imgur.com/K09XoVs.png',
    'https://i.imgur.com/pMVyrWp.png',
    'https://i.imgur.com/jRGDNPq.png',
    'https://i.imgur.com/5NMK4yB.png',
    'https://i.imgur.com/Q64S32h.png',
    'https://i.imgur.com/P2SKHyP.png',
    'https://i.imgur.com/3JQoDlZ.png',
    'https://i.imgur.com/uDBzYUS.png',
    'https://i.imgur.com/XQLUkxS.png',
    'https://i.imgur.com/J5f3AsT.png',
    'https://i.imgur.com/MM34JqO.png',
    'https://i.imgur.com/wSze3eZ.png',
    'https://i.imgur.com/ml9sBMb.png',
    'https://i.imgur.com/hne06Co.png',
    'https://i.imgur.com/alSKVHi.png',
    'https://i.imgur.com/NeUBLnF.png',
    'https://i.imgur.com/TSMdNFH.png',
    'https://i.imgur.com/QZCNH6p.png',
    'https://i.imgur.com/xA41cdx.png',
    'https://i.imgur.com/7JlxlEU.png',
    'https://i.imgur.com/UpObWyP.png',
    'https://i.imgur.com/MtfMfIk.png',
    'https://i.imgur.com/fsRQ7oj.png',
    'https://i.imgur.com/XYNBqu0.png'
]

crime_caught_images = [
    'https://i.imgur.com/RJ7Fdd4.jpeg',
    'https://i.imgur.com/meL2Fn5.jpeg',
    'https://i.imgur.com/8qL6xrS.png',
    'https://i.imgur.com/98JH8SK.png',
    'https://i.imgur.com/oQAiy9j.png',
    'https://i.imgur.com/KE0aMBs.png',
    'https://i.imgur.com/ljNFGCO.png',
    'https://i.imgur.com/UqW4vKJ.png',
    'https://i.imgur.com/auI1JaC.png',
    'https://i.imgur.com/IADiS93.jpeg',
    'https://i.imgur.com/pKk35vW.png',
    'https://i.imgur.com/tiqP677.png',
    'https://i.imgur.com/WOQFwN9.png',
    'https://i.imgur.com/3BWNc91.png',
    'https://i.imgur.com/fIzc3IM.png'
]

drug_deal_successful_images = [
    'https://i.imgur.com/rRCtS7h.png',
    'https://i.imgur.com/IBSmJGF.png',
    'https://i.imgur.com/PgeL1Xp.png'
]

attack_user_images = [
    'https://i.imgur.com/twoS38X.png',
    'https://i.imgur.com/hDxlUG4.png',
    'https://i.imgur.com/qOIjXbW.png',
    'https://i.imgur.com/gXKpd83.png',
    'https://i.imgur.com/hTLC2pi.png',
    'https://i.imgur.com/XsBWZwF.png',
    'https://i.imgur.com/SJ9RrrJ.png',
    'https://i.imgur.com/NSrSImU.png',
    'https://i.imgur.com/910l3ao.png',
    'https://i.imgur.com/1V3Mj4Q.png',
    'https://i.imgur.com/7feS6cn.png',
    'https://i.imgur.com/eqXvJEP.png',
    'https://i.imgur.com/1QyP7HQ.png',
    'https://i.imgur.com/AwK90s4.png',
    'https://i.imgur.com/6PvH0tF.png',
    'https://i.imgur.com/4g0cWYq.png',
    'https://i.imgur.com/9m1pYiX.png',
    'https://i.imgur.com/3kBuFVW.png',
    'https://i.imgur.com/fF6GyAM.png',
    'https://i.imgur.com/goKi7ET.png',
    'https://i.imgur.com/9M43qdq.png',
    'https://i.imgur.com/zKIC5rV.png'
]

user_killed_images = [
    'https://i.imgur.com/bfXL8rE.jpeg',
    'https://i.imgur.com/GaYHLr2.jpeg',
    'https://i.imgur.com/AmnDITf.jpeg',
    'https://i.imgur.com/ylXiHbL.png',
    'https://i.imgur.com/MdnTcph.png',
    'https://i.imgur.com/txviVpy.png',
    'https://i.imgur.com/zpb0tdq.png',
    'https://i.imgur.com/RGIdpJu.png',
    'https://i.imgur.com/BrAHMOT.png',
    'https://i.imgur.com/iXMbmbr.png',
    'https://i.imgur.com/cfrmFV1.png',

]

substances_data = [
    {
        "id": 1,
        "name": "benzos",
        "min_price": 800,
        "max_price": 25000,
        "min_price_change": 2000,
        "max_price_change": 4000,
        "max_amount": 30
    },
    {
        "id": 2,
        "name": "weed",
        "min_price": 3000,
        "max_price": 30000,
        "min_price_change": 3000,
        "max_price_change": 5000,
        "max_amount": 30
    },
    {
        "id": 3,
        "name": "pills",
        "min_price": 4000,
        "max_price": 50000,
        "min_price_change": 4500,
        "max_price_change": 6000,
        "max_amount": 20
    },
    {
        "id": 4,
        "name": "heroin",
        "min_price": 5000,
        "max_price": 60000,
        "min_price_change": 6000,
        "max_price_change": 8500,
        "max_amount": 20
    },
    {
        "id": 5,
        "name": "amphetamines",
        "min_price": 7000,
        "max_price": 80000,
        "min_price_change": 5500,
        "max_price_change": 10000,
        "max_amount": 15
    },
    {
        "id": 6,
        "name": "shrooms",
        "min_price": 12000,
        "max_price": 120000,
        "min_price_change": 8000,
        "max_price_change": 12000,
        "max_amount": 15
    },
    {
        "id": 7,
        "name": "cocaine",
        "min_price": 30000,
        "max_price": 250000,
        "min_price_change": 15000,
        "max_price_change": 24000,
        "max_amount": 10
    }
]

police_activity_range = {
    'min_activity': 0,
    'max_activity': 0.6
}

drug_dealing_jail = {
    'min_time': 150,
    'max_time': 320
}

drug_dealing_escape_chance_multiplier = 1.5
drug_dealing_police_dont_arrest = 0.15
drug_price_magic_number = 1230
drug_market_price_change_period = 3600

gun_data = [
    {
        'id': 0,
        'name': 'brass-knuckles',
        'price': 100,
        'min_damage': 5,
        'max_damage': 9,
        'effectiveness': 1,
        'break_chance': 0.3
    },
    {
        'id': 1,
        'name': 'crowbar',
        'price': 200,
        'min_damage': 7,
        'max_damage': 9,
        'effectiveness': 1.1,
        'break_chance': 0.45
    },
    {
        'id': 2,
        'name': 'knife',
        'price': 250,
        'min_damage': 6,
        'max_damage': 10,
        'effectiveness': 1.15,
        'break_chance': 0.6
    },
    {
        'id': 3,
        'name': 'pistol',
        'price': 800,
        'min_damage': 12,
        'max_damage': 17,
        'effectiveness': 1.2,
        'break_chance': 0.24
    },
    {
        'id': 4,
        'name': 'revolver',
        'price': 1000,
        'min_damage': 14,
        'max_damage': 20,
        'effectiveness': 1.23,
        'break_chance': 0.3
    },
    {
        'id': 5,
        'name': 'smg',
        'price': 1700,
        'min_damage': 10,
        'max_damage': 26,
        'effectiveness': 1.27,
        'break_chance': 0.3
    },
    {
        'id': 6,
        'name': 'shotgun',
        'price': 2400,
        'min_damage': 9,
        'max_damage': 35,
        'effectiveness': 1.3,
        'break_chance': 0.15
    },
    {
        'id': 7,
        'name': 'semi-automatic-rifle',
        'price': 3500,
        'min_damage': 16,
        'max_damage': 36,
        'effectiveness': 1.5,
        'break_chance': 0.3
    },
    {
        'id': 8,
        'name': 'machine-gun',
        'price': 7000,
        'min_damage': 22,
        'max_damage': 32,
        'effectiveness': 1.7,
        'break_chance': 0.7
    },
    {
        'id': 9,
        'name': 'sniper-rifle',
        'price': 12500,
        'min_damage': 37,
        'max_damage': 42,
        'effectiveness': 1.86,
        'break_chance': 0.18
    },
    {
        'id': 10,
        'name': 'autosniper',
        'price': 12500,
        'min_damage': 30,
        'max_damage': 47,
        'effectiveness': 1.9,
        'break_chance': 0.18
    },
    {
        'id': 11,
        'name': 'assault-rifle',
        'price': 12500,
        'min_damage': 2,
        'max_damage': 47,
        'effectiveness': 1.9,
        'break_chance': 0.18
    }
]

gun_sell_price_penalty = 0.73
gun_storage_limit = 24

death_cooldown = 1500
death_money_loss_ratio = 0.94
kill_money_gain_ratio = 0.6
attacked_money_loss_ratio = 0.019
attack_money_gain_ratio = 0.013
attack_level_requirement = 2

attack_user_xp_multiplier = 130
killed_user_xp_multiplier = 440
attack_cooldown = 555

levels = [
    {
        'id': 1,
        'xp': 0,
        'crime_factor': 0.85,
    },
    {
        'id': 2,
        'xp': 1200,
        'crime_factor': 0.9,
    },
    {
        'id': 3,
        'xp': 2500,
        'crime_factor': 0.95,
    },
    {
        'id': 4,
        'xp': 4000,
        'crime_factor': 1.0,
    },
    {
        'id': 5,
        'xp': 7000,
        'crime_factor': 1.05,
    },
    {
        'id': 6,
        'xp': 12000,
        'crime_factor': 1.1,
    },
    {
        'id': 7,
        'xp': 20000,
        'crime_factor': 1.15,
    },
    {
        'id': 8,
        'xp': 30000,
        'crime_factor': 1.2,
    },
    {
        'id': 9,
        'xp': 45000,
        'crime_factor': 1.25,
    },
    {
        'id': 10,
        'xp': 70000,
        'crime_factor': 1.3,
    },
    {
        'id': 11,
        'xp': 100000,
        'crime_factor': 1.4,
    },
    {
        'id': 12,
        'xp': 140000,
        'crime_factor': 1.5,
    },
    {
        'id': 13,
        'xp': 190000,
        'crime_factor': 1.6,
    },
    {
        'id': 14,
        'xp': 270000,
        'crime_factor': 1.7,
    },
    {
        'id': 15,
        'xp': 370000,
        'crime_factor': 1.8,
    },
    {
        'id': 16,
        'xp': 480000,
        'crime_factor': 1.9,
    },
    {
        'id': 17,
        'xp': 600000,
        'crime_factor': 2.0,
    },
    {
        'id': 18,
        'xp': 750000,
        'crime_factor': 2.2,
    },
    {
        'id': 19,
        'xp': 1000000,
        'crime_factor': 2.4,
    },
    {
        'id': 20,
        'xp': 1500000,
        'crime_factor': 3.0,
    }
]

car_data = [
    {
        'id': 0,
        'name': 'Volkswagen Polo',
        'command': 'vw',
        'steal_chance': 0.31,
        'escape_chance': 0.5,
        'min_jail_time': 80,
        'max_jail_time': 110,
        'price': 3000
    },
    {
        'id': 1,
        'name': 'Opel Astra',
        'command': 'opel',
        'steal_chance': 0.3,
        'escape_chance': 0.51,
        'min_jail_time': 80,
        'max_jail_time': 110,
        'price': 3000
    },
    {
        'id': 2,
        'name': 'Toyota Yaris',
        'command': 'yaris',
        'steal_chance': 0.27,
        'escape_chance': 0.45,
        'min_jail_time': 80,
        'max_jail_time': 118,
        'price': 3500
    },
    {
        'id': 3,
        'name': 'Seat Ibiza',
        'command': 'seat',
        'steal_chance': 0.22,
        'escape_chance': 0.42,
        'min_jail_time': 90,
        'max_jail_time': 125,
        'price': 4200
    },
    {
        'id': 4,
        'name': 'Ford Fiesta',
        'command': 'ford',
        'steal_chance': 0.2,
        'escape_chance': 0.35,
        'min_jail_time': 100,
        'max_jail_time': 150,
        'price': 5400
    },
    {
        'id': 5,
        'name': 'Mazda 6',
        'command': 'mazda',
        'steal_chance': 0.18,
        'escape_chance': 0.2,
        'min_jail_time': 170,
        'max_jail_time': 220,
        'price': 9000
    },
    {
        'id': 6,
        'name': 'BMW e36',
        'command': 'bmw',
        'steal_chance': 0,
        'price': 15000
    },
    {
        'id': 7,
        'name': 'Audi A3',
        'command': 'audi',
        'steal_chance': 0,
        'price': 25000
    },
    {
        'id': 8,
        'name': 'Mercedes AMG GT',
        'command': 'benz',
        'steal_chance': 0,
        'price': 50000
    },
    {
        'id': 9,
        'name': 'Toyota Supra Mk4',
        'command': 'supra',
        'steal_chance': 0,
        'price': 75000
    },
    {
        'id': 10,
        'name': 'Nissan GT-R',
        'command': 'nissan',
        'steal_chance': 0,
        'price': 100000
    },
    {
        'id': 11,
        'name': 'Ferrari Roma',
        'command': 'ferrari',
        'steal_chance': 0,
        'price': 200000
    },
    {
        'id': 12,
        'name': 'Rolls Royce Phantom',
        'command': 'phantom',
        'steal_chance': 0,
        'price': 500000
    },
]

race_money_car_price_ratio = 0.3
race_gain_multiplier_min = 0.7
race_gain_multiplier_max = 1.3
race_xp_gain_multiplier_min = 0.9
race_xp_gain_multiplier_max = 1.1
car_theft_level_scaling = 1.48
car_storage_limit = 24
car_repair_price_factor = 0.27
