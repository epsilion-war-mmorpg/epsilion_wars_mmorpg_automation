# [Epsilion War](https://t.me/epsilionwarbot?start=ref-537453818) MMORPG automation tool
---
[![tests](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/tests.yml)
[![linters](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/linters.yml/badge.svg?branch=master)](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/linters.yml)

todo video
todo description



### TODO
- update readme
- record a demo gif
- update github repo
- sigint and shutdown by time
- counters
- publish as package


### Pre-requirements
- [python 3.11+](https://www.python.org/downloads/)
- Telegram account and [API id+hash](https://docs.telethon.dev/en/stable/basic/signing-in.html#signing-in)
- Registration in game [registered here](https://t.me/epsilionwarbot?start=ref-537453818)

### Quick start
```bash
git clone https://github.com/esemi/epsilion_wars_mmorpg_automation.git
cd epsilion_wars_mmorpg_automation
python3.11 -m venv venv
source venv/bin/activate
pip install -U poetry pip setuptools
poetry install
cat > .env << EOF
telegram_api_id=%U_API_ID%
telegram_api_hash=%U_API_HASH%
EOF

poetry run grind        # for infinite grinding start
poetry run grind -t 35  # grinding for next 35 minutes
```

### Local run linters
```
poetry run flake8 epsilion_wars_mmorpg_automation/
```

### Local run MyPy
```
poetry run mypy epsilion_wars_mmorpg_automation/
```
