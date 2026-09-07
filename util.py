import random
import botdata


def format_crime_details(crime):
    crime_command = crime['command']
    crime_profits = f"${crime['min_profit']}-${crime['max_profit']}"
    crime_jail = f"{crime['min_jail_time']}s-{crime['max_jail_time']}s"
    return f'`{crime_command:17} {crime_profits:13} {crime_jail}`'


def check_event_based_on_probability(probability, opposite=False):
    if opposite:
        return True if random.uniform(0, 1) > probability else False

    return True if random.uniform(0, 1) < probability else False


def clamp_int(n, smallest, largest):
    return max(smallest, min(n, largest))


def get_police_activity_string(police_activity):
    if police_activity <= 0.1:
        return 'Очекуваме да не ве замараат многу од полицијата во следниот период. Полицајците се зафатени со други работи, тешко да фанат некој.'
    if police_activity <= 0.2:
        return 'Полицијата ќе претресува за дрога, ама ништо посериозно. Сепак, предлагаме да се пазите.'
    if police_activity <= 0.3:
        return 'Полицијата ќе превзема акции против дилерите во наредниот период. Може да продавате, ама пазете се!'
    if police_activity <= 0.4:
        return 'Полицијата фаќа дилери лево и десно. Ви предлагаме да продавате само на тие што ги знаете'
    if police_activity <= 0.5:
        return 'Полцијата спроведува акција за апцење на скоро сите дилери. Сега за сега, подобро е да одмарате.'
    return 'Полицијата спроведува интензивна акција за апцење на сите дилери на наркотици. ОГРОМЕН РИЗИК ПРИ ПРОДАВАЊЕ!'


def get_level_based_on_xp(xp):
    for level in botdata.levels[::-1]:
        if xp >= level['xp']:
            return level['id'] - 1
    return 1


def get_xp_to_next_level(level, xp):
    if level == 19:
        return 0
    xp_remaining = botdata.levels[level + 1]['xp'] - xp
    return xp_remaining


def get_formatted_min_secs(seconds):
    m, s = divmod(seconds, 60)
    return f"{m}m, {s}s"


damage_mult = 0.4
max_level = 20


def get_damage_multiplier_based_on_level(level):
    level += 1

    return damage_mult + ((level/max_level) * damage_mult)
