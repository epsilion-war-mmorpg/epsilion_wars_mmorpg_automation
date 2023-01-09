# Epsilion War mmorpg automation
[play now](https://t.me/epsilionwarbot?start=ref-537453818)

---
[![tests](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/tests.yml/badge.svg?branch=master)](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/tests.yml)
[![codecov](https://codecov.io/github/esemi/epsilion_wars_mmorpg_automation/branch/master/graph/badge.svg?token=4D3V7NMX9Q)](https://codecov.io/github/esemi/epsilion_wars_mmorpg_automation)
[![linters](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/linters.yml/badge.svg?branch=master)](https://github.com/esemi/epsilion_wars_mmorpg_automation/actions/workflows/linters.yml)

### TODO
- CI
- mvp - telegram auth
- mvp - simple grinding
- codecov
- update run docs (use telegram api-key)
- nice runner like poetry run grinding
- mvp - random awaits
- mvp - use specials
- mvp - raise if unknown state
- mvp - wait HP-level >= 70%
- mvp - random choice attack and block 
- mvp - graceful shutdown


### Pre-requirements
- [python 3.11+](https://www.python.org/downloads/)

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
debug=true
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
