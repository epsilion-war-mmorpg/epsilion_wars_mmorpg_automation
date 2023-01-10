# Epsilion War MMORPG automation
---

[![tests](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/tests.yml)
[![linters](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/linters.yml/badge.svg?branch=master)](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/linters.yml)


[play now](https://t.me/epsilionwarbot?start=ref-537453818)


### TODO
- mvp - random awaits
- nice runner like `poetry run grinding 10`
- update quick start
- record a demo gif


### Pre-requirements
- [python 3.11+](https://www.python.org/downloads/)
- Telegram account and [API id+hash](https://docs.telethon.dev/en/stable/basic/signing-in.html#signing-in)
- Game-character [registered here](https://t.me/epsilionwarbot?start=ref-537453818)

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

python -m app.grinding
```

### Local run linters
```
poetry run flake8 app/
```

### Local run MyPy
```
poetry run mypy app/
```
