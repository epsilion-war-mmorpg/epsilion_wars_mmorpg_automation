# Epsilion Trainer
---
[![tests](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/tests.yml)
[![linters](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/linters.yml/badge.svg?branch=master)](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/linters.yml)


Epsilion Trainer is an automated tool that allows users to quickly and easily level up their character in [Epsilion War MMORPG](https://t.me/epsilionwarbot?start=ref-537453818).
It will automatically control your character in the monster hunt area, instantly earning experience points, money and items.
With Epsilion Trainer, you can quickly become the strongest player on the server.

Good guide about grinding [here](https://teletype.in/@nathan_banana/3VVnxGQdp). 

### Setup
To run the Epsilion Trainer for the first time, you will need to:
1. Install [Python 3.11 or later](https://www.python.org/downloads/).
2. Generate a Telegram [API ID and hash](https://docs.telethon.dev/en/stable/basic/signing-in.html#signing-in).
3. [Register](https://t.me/epsilionwarbot?start=ref-537453818) for the game.
4. Download and install the latest version of Epsilion Trainer using the given commands.
```shell
git clone https://github.com/esemi/epsilion_wars_mmorpg_automation.git
cd epsilion_wars_mmorpg_automation
pip install -U poetry
poetry install --only main
```

5. Place the Telegram credentials (from step #2) in the `.env` file
```shell
cat > .env << EOF
telegram_api_id=U_API_ID
telegram_api_hash=U_API_HASH
EOF
```

### Run grind:
1. Use `poetry run grind -t 30` to start a workout with a time limit of thirty minutes.
2. To start a workout indefinitely, use `poetry run grind` without the -t flag


### TODO
- use combos by order (versus random choice)
- update github repo
- stop grinding when equip loss
- describe customer settings in readme
- record a demo gif
- publish as package

- desktop notifications about equip loss and battle failed
- print counters
- send stats to me


### Local run linters and tests
```shell
poetry install
poetry run flake8 epsilion_wars_mmorpg_automation/
poetry run mypy epsilion_wars_mmorpg_automation/
poetry run pytest
```
