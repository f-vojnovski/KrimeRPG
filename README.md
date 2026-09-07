# KrimeRPG

A crime-themed text RPG played entirely through Discord commands. It ran for about a year
on a Macedonian-language server and peaked at around 20 active players.

![bot-img](https://i.imgur.com/zCrzHnd.png)

Every action is a dice roll. A player types a command and the bot rolls against a success
chance. A win pays cash and XP. A loss usually means jail, which locks out every other
command until it expires. Levels raise the odds on everything, which is what brings the
expensive, low-probability jobs within reach. Player state lives in MongoDB.

## An example turn

Player-facing text is Macedonian, glossed here in English.

```
$signup
  Добредојде во светот на криминалот, filip. 👋🎉
  → Welcome to the world of crime, filip.

$crime pickpocket
  [embed] filip успешно го изврши криминалното дело!
          Заработени пари: 💵87    Добиено XP: 71
  → Job pulled off. Money earned, XP gained.

$crime pickpocket
  Вие извршивте криминал скоро. Обидете се повторно за 0m, 8s.
  → You pulled a job recently. Try again in 8s.

$stats
  Статистика за filip: Енергија: 🩸1000, Пари: 💵87, Ниво: 1, XP до следно ниво: 1129.
  → Health, money, level, XP to the next level.
```

## Commands

| Command | Effect |
| --- | --- |
| `$signup` / `$stats` | Create a player; check health, money, level and XP |
| `$crime <name>` | Attempt one of 5 unarmed jobs |
| `$armedcrime <name> <weapon>` | Attempt one of 7 higher-paying jobs, using a weapon you own |
| `$buydrugs` / `$selldrugs` / `$mydrugs` | Trade on and check stock from the black market |
| `$buygun` / `$sellgun` / `$myguns` | Buy, sell and list weapons |
| `$attack @player <weapon>` | Fight another player |
| `$heal` | Recover health for a cut of your balance |
| `$buybusiness <name>` | Buy one of 50 businesses |
| `$respawn` | Return to play after being killed |

## How the world moves

Two background jobs run on timers, which gave the server something happening between play
sessions.

Every hour, one job reprices the black market and posts the changes to a channel. Prices
pull back toward the middle of each item's range: the odds of a rise are the remaining
room below the ceiling over the item's full range. The same job rolls a global
police-activity level that every sale is checked against, and publishes it as an
in-character intelligence report rather than a number.

Every two hours, the other pays out to business owners and announces it publicly. A
business has one owner at a time, and the only way to take a good one is to kill whoever
owns it.

Fighting itself is open only during evening hours in the server's timezone, which kept it
inside the window the server was actually busy. A kill moves a large share of the victim's
balance to the attacker, benches the victim for 25 minutes, and frees up every business
they held.

## Architecture

nextcord on Python 3.8, with MongoDB through pymongo holding all player state, and the two
recurring economy jobs as `nextcord.ext.tasks` loops. Game content (jobs, weapons,
businesses, the level curve) lives as Python dicts in [botdata.py](botdata.py) and
[businessdata.py](businessdata.py) rather than database rows.

Replit stops idle repls after an hour, which would have taken the bot offline between
sessions. A small Flask server starts alongside the bot and UptimeRobot pings its public
URL on a schedule, so the repl never reads as idle. Embed images are hosted on imgur.

## Running it

Needs `BOT_TOKEN` and `MONGO_CONN_STRING` in the environment. Some things are wired to the
original deployment:

- `webserver.py`, which defines `keep_alive()`, is not in this repo.
- The channel IDs the background jobs post to are constants near the top of
  [main.py](main.py#L18-L19).
- The `substances`, `config_vars` and `business_collection` collections are read and
  updated but never created, so they need seeding before the first run.
- Car theft and street racing were designed but never shipped. Thirteen vehicles sit in
  [botdata.py](botdata.py) with no commands wired to them.
