Epsilion Trainer
---
TODO GIF

The Epsilion Trainer is an automated tool that allows users to quickly and easily level up their character in [the Epsilion War MMORPG](https://t.me/epsilionwarbot?start=ref-537453818).
It automatically controls your character and instantly earns experience points, money and items.
With Epsilion Trainer you can quickly become the strongest player on the server.

[![tests](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/tests.yml)
[![linters](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/linters.yml/badge.svg?branch=master)](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/linters.yml)


### Requirements
1. [Python 3.11 or later](https://www.python.org/downloads/) and [pip](https://pip.pypa.io/en/stable/installation/) 
2. Telegram [API ID and token](https://docs.telethon.dev/en/stable/basic/signing-in.html#signing-in)
3. [Registration](https://t.me/epsilionwarbot?start=ref-537453818) on the game.


### Installation
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


### Grinding:
Grinding will save you from having to fight annoying monsters in the hunting grounds. 
The Epsilion Trainer checks your health before searching for an enemy, choosing a random direction to attack and block, using combat tricks and collecting the reward. 
Sometimes you just need to take your character to repair equipment and open chests.

Just get your character to the right location, equip PVE and run the Epsilion Trainer with `grind`. 

If you prefer to hunt for a limited time, you can use `grind -t 30`: it will only hunt for 30 minutes, after which it will automatically shut down.

TODO GIF

#### Settings
You can change the settings in the .env file as follows

`minimum_hp_level_for_grinding`: Minimum HP level to begin hunting. Default level is 75%.

`notifications_enabled`: Send alerts about important events. On by default.

`auto_healing_enabled`: Using HP potions is enabled by default.

`stop_if_equip_broken`: Stop when something breaks. On by default.

`stop_if_captcha_fire`: Stop when captcha detected. Default is off.

`select_random_combo`: Choose a random combo shot from the available ones. On by default.

`skip_combo`: Skip the combo shots sometimes. On by default.

`captcha_solver_enabled`: Try to solve simple captcha automatically. Enabled by default.


### What about the captcha?
The Epsilion Trainer successfully solves simple text captcha. 
But it won't be able to solve numbers in a picture. 

Fortunately, there are some services that can help us. 
[One is already included](http://getcaptchasolution.com/r4gkdobk03). 
Just register there, top up your account with some $ and add your account key to settings.

You can have more information about registration and account funding on [their web site](http://getcaptchasolution.com/r4gkdobk03).   

You can also run the Epsilion Trainer in captcha-only help mode. Use the command `captcha-solver`.

In this mode, the tool will only help you solve the captcha automatically and nothing else.


#### Settings

`captcha_solver_enabled`: Try to solve simple captcha automatically. Enabled by default.

`notifications_enabled`: Send alerts about important events. On by default.

`anti_captcha_com_apikey`: your account key (ex: 172ea50b3d12345678de199546c66b20)


### What about the rules?
TL;DR Screw [the rules](https://teletype.in/@epsilionwar/HkPsNEfZL)


#### Feature-requests
- readme for customers
- publish as package
- daily-rewards tool
- fishing tool
- mover tool
- repair tool
