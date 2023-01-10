# Epsilion War mmorpg automation
[play now](https://t.me/epsilionwarbot?start=ref-537453818)

---
[![tests](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/tests.yml)
[![linters](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/linters.yml/badge.svg?branch=master)](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/linters.yml)

### TODO
- mvp - simple grinding
- mvp - random awaits
- mvp - use combos
- CI + badges
- nice runner like `poetry run grinding 10`
- update quick start
- record a demo gif


### Pre-requirements
- [python 3.11+](https://www.python.org/downloads/)
- [telegram account and API key](https://docs.telethon.dev/en/stable/basic/signing-in.html#signing-in)

### Local setup
```shell
$ git clone https://github.com/esemi/epsilion_wars_mmorpg_automation.git
$ cd epsilion_wars_mmorpg_automation
$ python3.11 -m venv venv
$ source venv/bin/activate
$ pip install -U poetry pip setuptools
$ poetry config virtualenvs.create false --local
$ poetry install
```

Create env file to override default config
```bash
cat > .env << EOF
telegram_api_id=%U_API_ID%
telegram_api_hash=%U_API_HASH%
EOF
```

### Local run tests
```shell
$ pytest --cov=app
```

### Local run app
```
python -m app.grinding
```

### Local run flake
```
poetry run flake8 app/
```
### Local run MyPy
```
poetry run mypy app/
```
