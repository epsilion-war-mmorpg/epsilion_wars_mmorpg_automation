# План технического и security-critical обновления проекта

Дата анализа: 2026-06-28
Репозиторий: `epsilion-war-mmorpg/epsilion_wars_mmorpg_automation`
Локальная ветка/рабочая копия: анализ выполнен по текущему checkout.

## 1. Краткое резюме

Проект является Python/Poetry CLI-автоматизацией для Telegram-клиента Telethon. Основные зоны риска:

- устаревший `poetry.lock` с зависимостями 2024 года;
- подтвержденные open Dependabot alerts в lock-файле: `h11 0.14.0`, `setuptools 72.1.0`, `pyasn1 0.6.0`, `idna 3.7`, `python-dotenv 1.0.1`, `pytest 8.3.2`, `Pygments 2.18.0`;
- GitHub Actions используют устаревшие major versions: `actions/checkout@v2`, `actions/setup-python@v1`;
- отсутствует явная конфигурация Dependabot в `.github/dependabot.yml`;
- отсутствует отдельный CI job для dependency audit;
- список GitHub Dependabot alerts уточнен через `gh api` 2026-06-28;
- проект работает с чувствительными артефактами: Telegram API credentials, AntiCaptcha API key, Telethon session file.

Цель обновления: закрыть текущие Dependabot/security alerts, обновить lock-файл без поломки runtime-сценариев, добавить автоматический контроль уязвимостей и зафиксировать процесс регулярного security triage.

## 2. Проверенный текущий контекст

### Runtime и пакетный менеджер

- `pyproject.toml` использует Poetry.
- Поддерживаемый Python: `^3.11`.
- CI запускает Python `3.11` и `3.12`.
- Локально установлен Python `3.12.10`.
- Локально не найден `poetry`.
- Локально не найден `pip-audit`.

### Основные runtime-зависимости из `pyproject.toml`

- `telethon = "^1.34.0"`
- `httpx = "^0.27.0"`
- `pydantic-settings = "^2.2.1"`
- `desktop-notifier = "^3.5.6"`

### Фактические версии из `poetry.lock`

- `telethon 1.36.0`
- `httpx 0.27.0`
- `httpcore 1.0.5`
- `h11 0.14.0`
- `idna 3.7`
- `certifi 2024.7.4`
- `pydantic 2.8.2`
- `pydantic-settings 2.4.0`
- `desktop-notifier 3.5.6`
- `setuptools 72.1.0`
- `pytest 8.3.2`
- `pytest-asyncio 0.23.8`
- `mypy 1.11.1`
- `wemake-python-styleguide 0.18.0`
- `pytest-cov 4.1.0`
- `pytest-mock 3.14.0`
- `python-dotenv 1.0.1`
- `pyasn1 0.6.0`
- `Pygments 2.18.0`

### CI

Текущие workflow:

- `.github/workflows/tests.yml`
- `.github/workflows/linters.yml`

Проблемы:

- `actions/checkout@v2` устарел;
- `actions/setup-python@v1` устарел;
- Poetry устанавливается без pinning;
- нет cache для Poetry/pip;
- нет dependency audit;
- нет явных минимальных permissions для workflow;
- workflow запускаются только на `push`, без `pull_request` и расписания для регулярного security контроля.

### Секреты и чувствительные файлы

Положительные моменты:

- `.env` добавлен в `.gitignore`;
- `.epsilion_automation_session.session*` добавлен в `.gitignore`;
- `.sessions/*` добавлен в `.gitignore`.

Риски:

- `.env.example` содержит примерный Telegram API ID/hash и custom channel. Значения выглядят тестовыми, но пример лучше сделать явно безопасным и недействительным.
- Telethon session хранится в предсказуемом файле `.epsilion_automation_session`. Это приемлемо для локального CLI, но требует документированных прав доступа и запрета на публикацию session-файла.
- AntiCaptcha client логирует полный response. Нужно проверить, не возвращает ли провайдер в response чувствительные поля, баланс, account metadata или диагностические данные.

## 3. GitHub Dependabot alerts

Источник проверки: GitHub Dependabot API через `gh api repos/epsilion-war-mmorpg/epsilion_wars_mmorpg_automation/dependabot/alerts --paginate`, выполнено 2026-06-28. Ниже зафиксирован фактический snapshot alerts из Security tab.

### Open alerts

| Alert | Severity | Package | Current | Patched | Advisory | CVE | Manifest |
| --- | --- | --- | --- | --- | --- | --- | --- |
| #13 | critical | `h11` | `0.14.0` | `0.16.0` | `GHSA-vqfr-h8mv-ghfj` | `CVE-2025-43859` | `poetry.lock` |
| #14 | high | `setuptools` | `72.1.0` | `78.1.1` | `GHSA-5rjg-fvgr-3xxf` | `CVE-2025-47273` | `poetry.lock` |
| #15 | high | `pyasn1` | `0.6.0` | `0.6.3` | `GHSA-jr27-m4p2-rc6r` | `CVE-2026-30922` | `poetry.lock` |
| #20 | medium | `idna` | `3.7` | `3.15` | `GHSA-65pc-fj4g-8rjx` | `CVE-2026-45409` | `poetry.lock` |
| #19 | medium | `python-dotenv` | `1.0.1` | `1.2.2` | `GHSA-mf9w-mj56-hr94` | `CVE-2026-28684` | `poetry.lock` |
| #18 | medium | `pytest` | `8.3.2` | `9.0.3` | `GHSA-6w46-j5rx-g56g` | `CVE-2025-71176` | `poetry.lock` |
| #17 | low | `Pygments` | `2.18.0` | `2.20.0` | `GHSA-5239-wwwm-4pmq` | `CVE-2026-4539` | `poetry.lock` |

### P0. `h11 0.14.0`

- Alert: `#13`
- Severity: `critical`
- Advisory: `GHSA-vqfr-h8mv-ghfj`
- CVE: `CVE-2025-43859`
- Уязвимый диапазон: `<0.16.0`
- Минимальная исправленная версия: `0.16.0`
- Риск: lenient parsing chunked encoding, request smuggling при наличии несовместимого proxy/reverse proxy.
- Ссылка: https://github.com/python-hyper/h11/security/advisories/GHSA-vqfr-h8mv-ghfj

Действие:

- Обновить `h11` минимум до `0.16.0`.
- Так как `h11` приходит через `httpcore/httpx`, предпочтительно обновить весь HTTP stack: `httpx`, `httpcore`, `h11`, `idna`, `certifi`.
- После обновления прогнать anti-captcha tests и любые тесты вокруг `httpx.AsyncClient`.

### P0. `setuptools 72.1.0`

- Alert: `#14`
- Severity: `high`
- Advisory: `GHSA-5rjg-fvgr-3xxf`
- CVE: `CVE-2025-47273`
- Уязвимый диапазон: `<78.1.1`
- Минимальная исправленная версия: `78.1.1`
- Риск: path traversal в `PackageIndex.download`, потенциальная arbitrary file write в контексте процесса.
- Ссылка: https://github.com/pypa/setuptools/security/advisories/GHSA-5rjg-fvgr-3xxf

Действие:

- Обновить lock так, чтобы `setuptools >=78.1.1`.
- Проверить, не блокирует ли обновление `wemake-python-styleguide 0.18.0` или его transitive dependencies.
- Если resolver не может поднять `setuptools`, обновлять dev-tooling отдельным PR.

### P0. `pyasn1 0.6.0`

- Alert: `#15`
- Severity: `high`
- Advisory: `GHSA-jr27-m4p2-rc6r`
- CVE: `CVE-2026-30922`
- Уязвимый диапазон: `<=0.6.2`
- Минимальная исправленная версия: `0.6.3`
- Риск: denial-of-service через unbounded recursion.
- Текущий путь: transitive dependency, используется через `rsa`, который используется `telethon`.

Действие:

- Обновить `pyasn1 >=0.6.3`.
- Проверить, что `rsa` и `telethon` остаются совместимыми.
- Прогнать тесты импорта и сценарии, где создается `TelegramClient`.

### P1. `idna 3.7`

- Alert: `#20`
- Severity: `medium`
- Advisory: `GHSA-65pc-fj4g-8rjx`
- CVE: `CVE-2026-45409`
- Уязвимый диапазон: `<3.15`
- Минимальная исправленная версия: `3.15`
- Риск: resource consumption / denial-of-service при специально сформированном input в `idna.encode()`.
- Ссылка: https://github.com/kjd/idna/security/advisories/GHSA-65pc-fj4g-8rjx

Действие:

- Обновить `idna >=3.15`.
- Дополнительно проверить, принимает ли проект пользовательские домены/URL. Сейчас прямой ввод доменов почти отсутствует, поэтому runtime-риск ниже, но dependency alert должен быть закрыт.

### P1. `python-dotenv 1.0.1`

- Alert: `#19`
- Severity: `medium`
- Advisory: `GHSA-mf9w-mj56-hr94`
- CVE: `CVE-2026-28684`
- Уязвимый диапазон: `<1.2.2`
- Минимальная исправленная версия: `1.2.2`
- Риск: symlink following в `set_key`, потенциальная arbitrary file overwrite при cross-device rename fallback.
- Текущий путь: transitive dependency `pydantic-settings -> python-dotenv`.

Действие:

- Обновить `python-dotenv >=1.2.2`, обычно через обновление `pydantic-settings` или lock refresh transitive dependencies.
- Проверить загрузку `.env` и отсутствие регрессий в `AppSettings`.

### P1. `pytest 8.3.2`

- Alert: `#18`
- Severity: `medium`
- Advisory: `GHSA-6w46-j5rx-g56g`
- CVE: `CVE-2025-71176`
- Уязвимый диапазон: `<9.0.3`
- Минимальная исправленная версия: `9.0.3`
- Риск: vulnerable tmpdir handling.
- Текущий путь: dev dependency.

Действие:

- Обновить `pytest >=9.0.3`.
- Проверить совместимость `pytest-asyncio`, `pytest-cov`, `pytest-mock`.
- Если `wemake-python-styleguide` или старые плагины конфликтуют, выносить dev-tooling refresh отдельным PR, но alert не dismiss без обоснования.

### P2. `Pygments 2.18.0`

- Alert: `#17`
- Severity: `low`
- Advisory: `GHSA-5239-wwwm-4pmq`
- CVE: `CVE-2026-4539`
- Уязвимый диапазон: `<2.20.0`
- Минимальная исправленная версия: `2.20.0`
- Риск: ReDoS из-за inefficient regex for GUID matching.
- Текущий путь: dev/transitive dependency, вероятно через lint/docs/tooling.

Действие:

- Обновить `Pygments >=2.20.0`.
- Проверить flake8/wemake цепочку и отсутствие конфликтов.

### Fixed historical alerts

GitHub Dependabot также показывает уже fixed alerts:

- `#12 setuptools`, `GHSA-cx63-2mw6-8hw5`, `CVE-2024-6345`, fixed 2024-08-13;
- `#10 idna`, `GHSA-jjg7-2v4v-x38h`, `CVE-2024-3651`, fixed 2024-05-01;
- `#9 GitPython`, `GHSA-2mqj-m65w-jghx`, `CVE-2024-22190`, fixed 2024-03-15;
- `#5 gitpython`, `GHSA-wfm5-v35h-vwf4`, `CVE-2023-40590`, fixed 2024-03-15;
- `#4 certifi`, `GHSA-xqr8-7jwr-rhp7`, `CVE-2023-37920`, fixed 2024-03-15;
- `#3 GitPython`, `GHSA-pr76-5cm5-w9cj`, `CVE-2023-40267`, fixed 2024-03-15;
- `#1 Pygments`, `GHSA-mrwq-x4v8-fh7p`, `CVE-2022-40896`, fixed 2024-03-15.

## 4. План работ по PR

### PR 1. Security lock refresh

Цель: минимально закрыть все open Dependabot alerts без крупных refactor.

Шаги:

1. Установить локальный инструментинг:

   ```bash
   python -m pip install --upgrade pip
   python -m pip install "poetry>=1.8,<2.0" pip-audit
   ```

2. Проверить Poetry metadata:

   ```bash
   poetry check
   poetry lock --no-update
   ```

3. Обновить security-critical packages и их transitive цепочки:

   ```bash
   poetry update h11 httpcore httpx idna setuptools pyasn1 rsa python-dotenv pydantic-settings pygments
   ```

4. Обновить dev-only alert по `pytest` отдельной командой, чтобы сразу увидеть tooling-конфликты:

   ```bash
   poetry update pytest pytest-asyncio pytest-cov pytest-mock
   ```

5. Если resolver не обновляет `setuptools`, `Pygments` или `pytest` из-за dev-зависимостей:

   ```bash
   poetry update setuptools pygments pytest wemake-python-styleguide flake8-bandit bandit
   ```

6. Проверить lock:

   ```bash
   poetry show h11 setuptools pyasn1 idna python-dotenv pytest pygments httpx httpcore
   poetry run pip-audit
   ```

7. Прогнать тесты:

   ```bash
   poetry run pytest --cov=epsilion_wars_mmorpg_automation
   poetry run mypy epsilion_wars_mmorpg_automation/
   poetry run flake8 epsilion_wars_mmorpg_automation/
   ```

Критерии готовности:

- `poetry.lock` содержит `setuptools >=78.1.1`;
- `poetry.lock` содержит `h11 >=0.16.0`;
- `poetry.lock` содержит `pyasn1 >=0.6.3`;
- `poetry.lock` содержит `idna >=3.15`;
- `poetry.lock` содержит `python-dotenv >=1.2.2`;
- `poetry.lock` содержит `pytest >=9.0.3`;
- `poetry.lock` содержит `Pygments >=2.20.0`;
- `poetry run pip-audit` не показывает high/critical findings;
- все unit tests проходят на Python 3.11 и 3.12;
- Dependabot alerts `#13`, `#14`, `#15`, `#20`, `#19`, `#18`, `#17` закрыты или перешли в fixed после merge.

### PR 2. Runtime dependency baseline update

Цель: обновить основные runtime-зависимости в рамках совместимых major/minor версий.

Обновить:

- `telethon`
- `httpx`
- `pydantic-settings`
- `desktop-notifier`
- transitive runtime packages: `pydantic`, `pydantic-core`, `anyio`, `certifi`, `sniffio`, `typing-extensions`.

Команды:

```bash
poetry update telethon httpx pydantic-settings desktop-notifier
poetry run pytest tests/actions tests/captcha tests/notifications tests/state tests/message_parsers tests/stats
```

Проверки совместимости:

- старт CLI entrypoints импортируется без ошибок;
- `TelegramClient` создается с прежними настройками;
- `AntiCaptchaClient` сохраняет контракт ошибок;
- настройки из `.env` продолжают парситься через `pydantic-settings`;
- тесты, использующие mocks Telethon, не ломаются из-за изменения типов/атрибутов.

Критерии готовности:

- lock обновлен;
- runtime tests проходят;
- README-команды установки остаются актуальными;
- нет новых Dependabot alerts по runtime-зависимостям.

### PR 3. Dev-tooling refresh

Цель: обновить тестовые и lint инструменты отдельно от runtime, чтобы не смешивать возможные style failures с security fix.

Обновить:

- `pytest`
- `pytest-asyncio`
- `pytest-cov`
- `pytest-mock`
- `mypy`
- `wemake-python-styleguide`
- transitive flake8 plugins.

Особое внимание:

- `wemake-python-styleguide 0.18.0` очень старый и может тянуть устаревшие flake8 plugins.
- Обновление `wemake` может вызвать большой объем style failures. Если это происходит, security PR не должен ждать полной миграции style guide.

Команды:

```bash
poetry update --only dev
poetry run pytest
poetry run mypy epsilion_wars_mmorpg_automation/
poetry run flake8 epsilion_wars_mmorpg_automation/
```

Критерии готовности:

- dev-зависимости не удерживают vulnerable transitive packages;
- mypy и flake8 проходят;
- изменения кода, если нужны, ограничены реальными несовместимостями tooling.

### PR 4. GitHub Actions hardening

Цель: обновить CI и сделать security проверки обязательными.

Изменить workflow:

- `actions/checkout@v2` -> `actions/checkout@v4`;
- `actions/setup-python@v1` -> `actions/setup-python@v5`;
- добавить `pull_request`;
- добавить минимальные permissions:

  ```yaml
  permissions:
    contents: read
  ```

- pin Poetry версию или использовать `pipx install poetry==...`;
- добавить cache:

  ```yaml
  cache: poetry
  ```

- разделить jobs:
  - `tests`;
  - `linters`;
  - `dependency-audit`.

Пример dependency audit job:

```yaml
security-audit:
  runs-on: ubuntu-latest
  permissions:
    contents: read
  steps:
    - uses: actions/checkout@v4
    - uses: actions/setup-python@v5
      with:
        python-version: "3.12"
        cache: "pip"
    - run: python -m pip install pip-audit poetry
    - run: poetry export --only main --without-hashes -f requirements.txt -o requirements.txt
    - run: pip-audit -r requirements.txt
```

Если текущая Poetry версия не поддерживает export без plugin, добавить `poetry-plugin-export` или использовать `pip-audit` по установленному environment.

Критерии готовности:

- CI запускается на `push` и `pull_request`;
- security audit job падает на vulnerable main dependencies;
- tests и linters проходят на Python 3.11/3.12;
- Actions больше не используют deprecated major versions.

### PR 5. Dependabot configuration

Цель: регулярные dependency PR и прозрачный triage.

Добавить `.github/dependabot.yml`:

```yaml
version: 2
updates:
  - package-ecosystem: "pip"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 5
    groups:
      runtime:
        patterns:
          - "telethon"
          - "httpx"
          - "pydantic*"
          - "desktop-notifier"
      dev-tools:
        dependency-type: "development"

  - package-ecosystem: "github-actions"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 3
```

Рекомендуемая политика:

- security alerts: merge/fix в течение 24-72 часов в зависимости от severity;
- runtime minor/patch: weekly batch;
- dev-tooling: отдельная группа, merge после CI;
- major updates: вручную, отдельный issue/PR с compatibility testing.

Критерии готовности:

- Dependabot создает PR для Poetry/Python и GitHub Actions;
- GitHub Security alerts больше не копятся без владельца;
- в README или docs описан triage-процесс.

### PR 6. Secret scanning и session hardening

Цель: снизить риск утечки Telegram credentials и session-файлов.

Шаги:

1. Проверить GitHub repository settings:
   - Secret scanning enabled;
   - Push protection enabled;
   - Dependabot alerts enabled;
   - Dependabot security updates enabled;
   - Private vulnerability reporting по необходимости.

2. Сделать `.env.example` явно безопасным:

   ```dotenv
   telegram_api_id=123456
   telegram_api_hash=replace_me
   anti_captcha_com_apikey=
   ```

3. Документировать чувствительные файлы:
   - `.env`;
   - `.epsilion_automation_session.session*`;
   - `.sessions/*`.

4. Рассмотреть настройку пути session-файла:

   ```python
   telethon_session_path: str = ".epsilion_automation_session"
   ```

   Это позволит пользователю хранить session вне репозитория, например в `~/.config/epsa/`.

5. Проверить логи:
   - не логировать API keys;
   - не логировать полный provider response, если он может содержать account metadata;
   - оставить request IDs/status/errors.

Критерии готовности:

- пример `.env.example` не похож на реальный секрет;
- документация предупреждает, что session-файл эквивалентен доступу к Telegram session;
- secret scanning включен в GitHub settings;
- логи не раскрывают чувствительные поля.

### PR 7. CodeQL/Bandit/security linting

Цель: добавить базовую SAST-проверку без переписывания проекта.

Шаги:

1. Добавить GitHub CodeQL workflow для Python:

   ```yaml
   name: codeql
   on:
     push:
     pull_request:
     schedule:
       - cron: "0 6 * * 1"
   permissions:
     security-events: write
     packages: read
     actions: read
     contents: read
   jobs:
     analyze:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - uses: github/codeql-action/init@v3
           with:
             languages: python
         - uses: github/codeql-action/analyze@v3
   ```

2. Добавить Bandit как отдельный мягкий этап сначала:

   ```bash
   poetry add --group dev bandit[toml]
   poetry run bandit -r epsilion_wars_mmorpg_automation
   ```

3. После первого прохода решить, делать Bandit обязательным или только report-only.

Критерии готовности:

- CodeQL results появляются в Security tab;
- Bandit либо проходит, либо имеет зафиксированный baseline с объясненными suppressions;
- новые security findings не игнорируются без issue.

## 5. Проверка GitHub Dependabot alerts

Команда для повторной проверки списка alerts:

```bash
gh api repos/epsilion-war-mmorpg/epsilion_wars_mmorpg_automation/dependabot/alerts --paginate \
  --jq '.[] | {
    number,
    state,
    package: .dependency.package.name,
    ecosystem: .dependency.package.ecosystem,
    manifest: .dependency.manifest_path,
    severity: .security_advisory.severity,
    ghsa: .security_advisory.ghsa_id,
    cve: .security_advisory.cve_id,
    summary: .security_advisory.summary,
    vulnerable: .security_vulnerability.vulnerable_version_range,
    patched: .security_vulnerability.first_patched_version.identifier,
    created_at,
    dismissed_at,
    fixed_at
  }'
```

Ожидаемый triage:

- сопоставить каждый alert с `poetry.lock`;
- зафиксировать package, current version, patched version, severity, exploitability;
- если alert уже закрыт локальным update, дождаться GitHub re-scan после merge;
- если alert в dev-only dependency, решать отдельно: update dev stack или dismiss only если alert недостижим в runtime и есть понятное обоснование;
- dismiss использовать только с причиной, а не вместо обновления.

## 6. Guardrails против поломки приложения

Главный принцип: security update должен быть маленьким, наблюдаемым и обратимым. Нельзя смешивать обновление зависимостей, рефакторинг, изменение логики бота и косметические правки в одном PR.

### Dependency update guardrails

- Не запускать широкий `poetry update` первым шагом. Сначала обновлять только пакеты из open alerts и минимальные transitive цепочки.
- Делить обновления на runtime и dev-only. `pytest`, `Pygments`, `wemake`, `flake8` не должны блокировать срочное закрытие runtime alerts, если они создают большой tooling churn.
- В каждом PR фиксировать diff lock-файла:

  ```bash
  git diff -- pyproject.toml poetry.lock
  poetry show --tree h11 httpx httpcore idna setuptools pyasn1 rsa python-dotenv pytest pygments
  ```

- Если resolver тянет крупный major update вне списка alerts, останавливать PR и явно решать: нужен ли этот пакет в текущем security batch.
- Не менять Python support range (`^3.11`) в security PR, если это не требуется конкретной patched version.
- Не удалять старые constraints из `pyproject.toml` без отдельного объяснения, какие alerts они блокировали.

### Test guardrails

Минимальный обязательный набор перед merge:

```bash
poetry check
poetry run pytest --cov=epsilion_wars_mmorpg_automation
poetry run mypy epsilion_wars_mmorpg_automation/
poetry run flake8 epsilion_wars_mmorpg_automation/
poetry run pip-audit
```

Дополнительные targeted checks:

- после `httpx/httpcore/h11/idna`: `poetry run pytest tests/captcha/anti_captcha tests/captcha`;
- после `pyasn1/rsa/telethon`: `poetry run pytest tests/actions tests/state tests/message_parsers`;
- после `python-dotenv/pydantic-settings`: добавить и прогнать тест загрузки `.env`;
- после `pytest/pytest-asyncio`: прогнать весь async test suite, не только smoke tests.

Нельзя мержить, если:

- тесты падают из-за реального изменения поведения, а не только из-за устаревшей проверки;
- `pip-audit` всё еще показывает open high/critical по main dependencies;
- Dependabot alert остается open после merge без понятного объяснения;
- lock-файл обновил десятки unrelated packages без причины.

### Runtime smoke guardrails

Перед выпуском обновления выполнить smoke checks без отправки команд в игру:

```bash
poetry run python -c "import epsilion_wars_mmorpg_automation.cli"
poetry run python -c "from epsilion_wars_mmorpg_automation.settings import app_settings; print(app_settings.trainer_name)"
poetry run python -c "from epsilion_wars_mmorpg_automation.telegram_client import client; print(client.session.filename)"
```

Для сетевых интеграций использовать mocks, а не реальные внешние side effects:

- Telegram: мокать `TelegramClient.send_message`, `get_entity`, `get_input_entity`, `download_media`;
- AntiCaptcha: мокать `httpx.AsyncClient.post`, отдельно проверять `HTTPError`, invalid JSON-like response и provider error code;
- desktop notifications: оставлять существующий mock/тестовый режим, не требовать GUI окружение в CI.

### Settings and secrets guardrails

- Добавить тест, который создает временный `.env` и проверяет parsing ключевых полей: `telegram_api_id`, `telegram_api_hash`, `anti_captcha_com_apikey`, bool flags, `repair_locations_path`.
- Проверить, что `app_settings` не логирует секреты целиком.
- Не менять путь Telethon session в том же PR, где обновляются зависимости. Это отдельный behavioral change.
- Если добавляется настраиваемый `telethon_session_path`, дефолт должен остаться прежним: `.epsilion_automation_session`.

### Rollback guardrails

- Каждый security PR должен содержать только один логический batch, чтобы rollback был обычным revert commit.
- Перед merge сохранить список текущих fixed targets: `h11>=0.16.0`, `setuptools>=78.1.1`, `pyasn1>=0.6.3`, `idna>=3.15`, `python-dotenv>=1.2.2`, `pytest>=9.0.3`, `Pygments>=2.20.0`.
- Если после merge ломается runtime, сначала revert PR целиком, затем повторить update меньшими группами:
  - HTTP stack: `h11/httpcore/httpx/idna/certifi`;
  - Telegram crypto stack: `pyasn1/rsa/telethon`;
  - settings stack: `python-dotenv/pydantic-settings/pydantic`;
  - dev stack: `pytest/Pygments/wemake/flake8`.

### Release guardrails

- Выпускать dependency update как patch release, если публичная версия проекта используется пользователями.
- В changelog/release notes явно указать, что update закрывает Dependabot alerts и не должен менять поведение бота.
- После merge вручную проверить GitHub Security tab: alerts `#13`, `#14`, `#15`, `#20`, `#19`, `#18`, `#17` должны перейти в `fixed`.
- Если alert не закрылся из-за transitive resolver, не dismiss сразу: сначала проверить итоговую версию в `poetry.lock`.

## 7. Риски совместимости

### Telethon

Риск: изменения в event model, message/button types, session handling.

Проверки:

- `tests/actions/*`
- `tests/state/*`
- `tests/message_parsers/*`
- ручной smoke import всех CLI entrypoints:

  ```bash
  poetry run python -c "import epsilion_wars_mmorpg_automation.cli"
  ```

### httpx/httpcore/h11

Риск: изменения exceptions, timeout behavior, transport defaults.

Проверки:

- `tests/captcha/anti_captcha/*`
- отдельный тест на обработку `httpx.HTTPError`;
- отсутствие логирования API key.

### pydantic-settings

Риск: изменения parsing `.env`, bool/list/set coercion, BaseSettings config.

Проверки:

- добавить тесты на загрузку ключевых env-полей;
- проверить `repair_locations_path`, `enabled_potions`, `enabled_scrolls`, `combo_*`.

### wemake/flake8/mypy

Риск: большой объем новых lint/type errors.

Тактика:

- не блокировать security lock refresh на full tooling modernization;
- при необходимости временно обновить только vulnerable transitive packages;
- вынести style migrations в отдельные PR.

## 8. Рекомендуемый порядок выполнения

1. Создать issue/checklist по open alerts `#13`, `#14`, `#15`, `#20`, `#19`, `#18`, `#17`.
2. Сделать PR 1 с минимальным security lock refresh.
3. Дождаться прохождения tests/linters и GitHub re-scan.
4. Сделать PR 4 с GitHub Actions hardening.
5. Добавить PR 5 с Dependabot config.
6. Сделать PR 2 runtime baseline update.
7. Сделать PR 3 dev-tooling refresh, если он не был полностью закрыт в PR 1.
8. Включить/проверить secret scanning и CodeQL.
9. Обновить README/docs с security process.

## 9. Definition of Done

Security update считается завершенным, когда:

- все текущие open Dependabot alerts `#13`, `#14`, `#15`, `#20`, `#19`, `#18`, `#17` закрыты или имеют документированное triage-решение;
- выполнены guardrails из раздела 6: lock diff проверен, smoke checks выполнены, unrelated updates вынесены или объяснены;
- `poetry.lock` не содержит известных vulnerable versions для main dependencies;
- `pip-audit` проходит в CI;
- GitHub Actions обновлены до актуальных major versions;
- Dependabot настроен для Poetry/Python и GitHub Actions;
- секреты и session-файлы описаны и игнорируются;
- тесты, mypy и flake8 проходят на поддерживаемых Python версиях;
- есть rollback path: предыдущий lock-файл можно вернуть отдельным revert commit, если runtime smoke testing выявит несовместимость.

## 10. Команды для финального локального контроля

```bash
poetry check
poetry lock --no-update
poetry run pytest --cov=epsilion_wars_mmorpg_automation
poetry run mypy epsilion_wars_mmorpg_automation/
poetry run flake8 epsilion_wars_mmorpg_automation/
poetry run pip-audit
git diff -- pyproject.toml poetry.lock .github docs
```

Если Poetry установлен только через pipx:

```bash
pipx install poetry
poetry self add poetry-plugin-export
```

## 11. Ссылки

- GitHub Dependabot alerts: https://github.com/epsilion-war-mmorpg/epsilion_wars_mmorpg_automation/security/dependabot
- Setuptools advisory: https://github.com/pypa/setuptools/security/advisories/GHSA-5rjg-fvgr-3xxf
- h11 advisory: https://github.com/python-hyper/h11/security/advisories/GHSA-vqfr-h8mv-ghfj
- idna advisory: https://github.com/kjd/idna/security/advisories/GHSA-65pc-fj4g-8rjx
- pyasn1 advisory: https://github.com/advisories/GHSA-jr27-m4p2-rc6r
- python-dotenv advisory: https://github.com/advisories/GHSA-mf9w-mj56-hr94
- pytest advisory: https://github.com/advisories/GHSA-6w46-j5rx-g56g
- Pygments advisory: https://github.com/advisories/GHSA-5239-wwwm-4pmq
- pip-audit: https://github.com/pypa/pip-audit
- Dependabot configuration: https://docs.github.com/en/code-security/dependabot/dependabot-version-updates/configuration-options-for-the-dependabot.yml-file
- CodeQL for Python: https://docs.github.com/en/code-security/code-scanning/introduction-to-code-scanning/about-code-scanning-with-codeql

## 12. Статус исполнения на 2026-07-01

Выполнен PR 1 / security lock refresh в локальной ветке.

Обновленные версии, закрывающие текущие Dependabot alerts:

| Package | Было в lock | Стало в lock/env | Минимум из alert | Статус |
| --- | --- | --- | --- | --- |
| `h11` | `0.14.0` | `0.16.0` | `0.16.0` | patched |
| `setuptools` | `72.1.0` | `80.10.2` | `78.1.1` | patched, зафиксировано `<81` из-за `flake8-commas/pkg_resources` |
| `pyasn1` | `0.6.0` | `0.6.3` | `0.6.3` | patched |
| `idna` | `3.7` | `3.18` | `3.15` | patched |
| `python-dotenv` | `1.0.1` | `1.2.2` | `1.2.2` | patched |
| `pytest` | `8.3.2` | `9.1.1` | `9.0.3` | patched |
| `Pygments` | `2.18.0` | `2.20.0` | `2.20.0` | patched |

Дополнительно обновлены совместимые transitive/dev packages: `httpx 0.27.2`, `httpcore 1.0.9`, `rsa 4.9.1`, `pydantic-settings 2.14.2`, `pytest-asyncio 1.4.0`, `pytest-cov 7.1.0`, `pytest-mock 3.15.1`.

Гварды против регрессий:

- `setuptools` закреплен как `>=78.1.1,<81`, потому что `setuptools 81+` удаляет `pkg_resources` и ломает текущую цепочку `wemake-python-styleguide -> flake8-commas`;
- `AppSettings` получил `EPSA_DISABLE_DOTENV=1` и `EPSA_ENV_FILE`, чтобы тесты и CI не зависели от локального `.env`;
- `tests/conftest.py` отключает dotenv и удаляет локальный `DEBUG`, чтобы `pytest 9` и новый `pydantic-settings` не падали от пользовательского окружения;
- `DesktopNotifier` создается лениво только при включенных desktop notifications, чтобы импорт приложения не падал на Windows/winsdk, когда уведомления отключены;
- `.gitignore` дополнен локальными `.venv`, `.poetry-cache`, `.poetry-config`.

CI и dependency automation:

- `.github/workflows/tests.yml` и `.github/workflows/linters.yml` обновлены с `actions/checkout@v2` / `actions/setup-python@v1` до `actions/checkout@v7.0.0` / `actions/setup-python@v6.3.0`;
- workflow теперь запускаются на `push` и `pull_request`, имеют минимальные `permissions: contents: read` и отключают dotenv через `EPSA_DISABLE_DOTENV=1`;
- Poetry в CI зафиксирован как `poetry==1.8.5`, чтобы локальный и CI resolver были ближе друг к другу;
- добавлен `.github/workflows/security-audit.yml` с `pip-audit==2.10.1`, запуском на `push`, `pull_request` и weekly schedule;
- добавлен `.github/dependabot.yml` для Python/Poetry dependencies и GitHub Actions.

Локальная верификация:

```bash
python -m poetry check
python -m poetry run pytest --cov=epsilion_wars_mmorpg_automation
python -m poetry run mypy epsilion_wars_mmorpg_automation/
python -m poetry run flake8 epsilion_wars_mmorpg_automation/
```

Результат:

- `poetry check`: passed;
- `pytest`: `231 passed, 4 skipped`, coverage total `47%`;
- `mypy`: `Success: no issues found in 59 source files`;
- `flake8`: passed, остаются предупреждения о deprecated `pkg_resources` от dev-tooling;
- YAML workflow/config parsing через проектный env: passed;
- `git diff --check`: passed;
- OSV batch audit по exported pinned requirements: `OSV vulnerabilities: 0`;
- `pip-audit` CLI в текущем локальном Python окружении не завершился из-за `CERTIFICATE_VERIFY_FAILED` при обращении к `pypi.org`; это нужно отдельно починить на уровне CA trust store или проверить в CI.

После push/merge нужно дождаться GitHub Dependabot re-scan. До re-scan GitHub Security tab может продолжать показывать старые open alerts, потому что локальный lock еще не попал в default branch.
