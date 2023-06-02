Epsilion Trainer
=================
[![tests](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/tests.yml)
[![linters](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/linters.yml/badge.svg?branch=master)](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/linters.yml)

The Epsilion Trainer is an automated tool that allows users to quickly and easily level up their character in [the Epsilion War MMORPG](https://t.me/epsilionwarbot?start=ref-537453818).
It automatically controls your character and instantly earns experience points, money and items.

Adopted for grades prior to T4.


Table of Contents
=================

* [What about the rules?](#what-about-the-rules)
* [Requirements](#requirements)
* [Installation](#installation)
* [Usage](#usage)
  * [Grinding](#grinding)
  * [Farming](#farming-experimental)
  * [Daily reward catcher](#daily-reward-catcher)
  * [Fishing](#fishing)
  * [Inventory](#inventory)
  * [What about the captcha?](#what-about-the-captcha)
* [Roadmap](#roadmap)
* [Developers](#developers)
  * [Run on server](#run-on-server)
  * [TData converter](#tdata-converter)
  * [Need more characters](#need-more-characters)


## What about the rules?
TL;DR Screw [the rules](https://teletype.in/@epsilionwar/HkPsNEfZL)


## Requirements
1. [Python 3.11 or later](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installation/) 
2. Telegram [API ID and token](https://docs.telethon.dev/en/stable/basic/signing-in.html#signing-in)
3. [Registration](https://t.me/epsilionwarbot?start=ref-537453818) on the game.


## Installation
Use the following commands to download and install the latest version of Epsilion Trainer
```shell
git clone https://github.com/esemi/epsilion_wars_mmorpg_automation.git
cd epsilion_wars_mmorpg_automation
pip install -U poetry pip setuptools
poetry install --only main
```

Place the telegram credentials (from the previous step) in the `.env` file using
```shell
cat > .env << EOF
telegram_api_id=U_API_ID
telegram_api_hash=U_API_HASH
EOF
```
The first time you use it, you'll need to log in to your Telegram account, but after that you'll be automatically logged in.

## Usage
### Grinding
Grinding will save you from having to fight annoying monsters in the hunting grounds. 
The Epsilion Trainer checks your health before searching for an enemy, choosing a random direction to attack and block, 
using combat tricks and collecting the reward. 
Sometimes you just need to take your character to repair_start equipment and open chests.

Just get your character to the right location, equip PVE and run the Epsilion Trainer with `grind`. 

If you prefer to hunt for a limited time, you can use `grind -t 30`: 
it will only hunt for 30 minutes, after which it will automatically shut down.

See also [grinding guide here](https://teletype.in/@esemiko/epsa-gringing) [RU lang].


##### Settings
You can change the settings in the .env file as follows

`minimum_hp_level_for_grinding`: Minimum HP level to begin grinding. Default level is 95%.

`notifications_enabled`: Send alerts about important events. On by default.

`auto_healing_enabled`: Using HP potions (I, II and III grades only). On by default.

`stop_if_equip_broken`: Stop when something breaks. On by default.

`select_combo_strategy`: A strategy for choosing a combo punch.
`simple` (always the first punch, default value), 
`random` (choose a random one available), 
`random-or-skip` (choose a random one available or skip turn), 
`disabled` (do not use combo punches), 
`tuned` [experimental] (choose combo based on its previous use). 

`stop_if_captcha_fire`: Stop when captcha detected. Default is off.

`captcha_solver_enabled`: Try to solve simple captcha automatically. On by default.

`use_backup_game_bot`: If the main game bot is down, you can try switching to the backup bot. Default is off.


### Farming [experimental]
**Warning: Experimental feature, may not be fully stable.**

Same as [Grinding](#grinding), but with automatic repair of equipment and return of the character to the location. 

You need the `farming` command to run it. 
The character remembers the name of the grinding location and will go to the town itself to repair things.

The character will go to a maximum of two locations away from the farming area to get things repaired. 
The names of the locations through which the path to the blacksmith passes must be set in `.env` (see settings below)
or when running the `farming --path "грейт,цирта"` command. 
The `--path` startup parameter has priority over the settings file.

Also returns the character to the farming area after death.

Items with a durability of 0/1 will not be repaired. 
Restoring the maximum durability of items is also up to you.

See also [farming math guide here](https://teletype.in/@esemiko/epsa-farming-economics) [RU lang].


##### Settings
`skip_random_vendor`: Skipping the random vendor you meet. On by default.

`skip_random_vendor_stop_words`: Prevents the random vendor from skipping for rare items. 
By default it does not skip `Свиток Кселеса` and `Безопасный свиток заточки [IV]`. 

`equip_farming_number`: Binding number of your farming equipment set. By default `1`.

`equip_travel_number`: Binding number of your travel gear. By default `2`.

`repair_locations_path`: The names of the places that make up the route to the blacksmith for repair. 
One word of the title, separated by commas, is sufficient (e.g. `грейт,цирта`). 
Not set by default.


### Daily reward catcher
If you find it inconvenient to keep track of your daily reward, you can use The Epsilon Trainer to handle it for you. 
The program automatically checks every hour to see if a reward has been made available, and it will attempt to collect it on your behalf. 

All you need to do is run The Epsilon Trainer and enter the `reward-catcher` command.


### Fishing
The Epsilion Trainer has a feature that allows your character to go fishing on their own. 
Give your character more rods, take him to the water and give him a `fishing` command.

The Epsilion Trainer will periodically check your character's energy level and start a fishing session when there's enough energy to do.
If any of your fishing rods break while fishing, the program will automatically replace them from your character's inventory.

Please keep in mind that it's important to only equip your character with fishing rods they can use effectively.

See also [fishing math guide here](https://teletype.in/@esemiko/epsa-fishing) [RU lang].


### Hunting
The Epsilion Trainer has a feature that allows your character to go hunting on their own. 
Give your character more bows, take him to the hunting area and give a `hunting` command.

The Epsilion Trainer will periodically check your character's energy level and start the hunt  when you have enough energy.
If any of your bows break, the software will automatically replace them.

Please remember that it is important that you only equip bows that you can use effectively.

See also [hunting math guide here](https://teletype.in/@esemiko/epsa-hunting) [RU lang].


### Inventory
The Epsilion Trainer knows how to inventory your character's resources.
Run `inventory` and after a short time you will see a message in your favourite Telegram chat showing all the recipes for sale. 

By default it takes a list of recipes, but you can get a list of other resources by using the `inventory -t` flag.


##### Settings
`favorites_enabled`: Send messages to telegram favorites chat. On by default.

`custom_channel_for_inventory`: Send inventory results to custom telegram chat 
(ex. `https://t.me/EpsilionWarBot` or `EpsilionWarBot`). 
Not set by default.


### What about the captcha?
The Epsilion Trainer successfully solves simple text captcha. 
But it won't be able to solve numbers in a picture. 

Fortunately, there are some services that can help us. 
[One is already included](http://getcaptchasolution.com/r4gkdobk03). 
Just register there, top up your account with some $ and add your account key to settings.

You can have more information about registration and account funding on [their web site](http://getcaptchasolution.com/r4gkdobk03).   

You can also run the Epsilion Trainer in captcha-only help mode. Use the command `captcha-solver`.

In this mode, the tool will only help you solve the captcha automatically and nothing else.


##### Settings
`anti_captcha_com_apikey`: your account key (ex: 172ea50b3d12345678de199546c66b20)


## Roadmap
- setup twink 7 - hunter
- setup twink 8 - leveling
- setup twink 8 - hunter
- setup twink 9 - leveling
- setup twink 9 - hunter
- make GIFs for readme
- readme on teletype page and change link in settings/readme.md
- contacts for support to readme.md

## Developers
### Run on server
To run The Epsilion Trainer on the server, you will need python and any supervisor (for automatic restart after failures, highly recommended).
For example:
```shell
adduser epsa
usermod -a -G supervisor epsa
cp ./etc/supervisor-example.conf /etc/supervisor/conf.d/epsa.conf
vi /etc/supervisor/conf.d/epsa.conf
service supervisor restart
```

### TData converter
If you plan to buy Telegram accounts, you will need a utility to convert credentials from tdata to .session (for Telethon library).
```shell
python etc/tdata_converter.py -f ~/.local/share/TelegramDesktop/tdata
```

### Need more characters?
The game allows you to have three characters per telegram account. 
If you need more, you will need new telegram accounts. 

You can buy them or create them yourself.
The algorithm for self-registration is as follows
- get a temporary phone number, for [example here](https://sms-activate.org/?ref=6431353)
- create an account with this number from telegram mobile app (or TelegramX if you are out of slots)
- set 2fa password, email, nickname and avatar 
- get your character into game using [a referral link](https://t.me/epsilionwarbot?start=ref-537453818)
- get authorisation for the Epsilion Trainer \([see step #2](#requirements)\)
- start grinding.

For a new account, I strongly recommend enabling the `slow_mode` flag in the settings. 
Otherwise, the Telegram may temporarily block the account for too many requests per minute.
