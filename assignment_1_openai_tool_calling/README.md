# Úkol 1 – OpenAI API a tool calling

Tento úkol demonstruje použití jazykového modelu společně s vlastní Pythonovou funkcí prostřednictvím tool callingu.

Aplikace analyzuje obsah pracovního e-mailu a rozhodne, zda obsahuje konkrétní požadavek. Pokud ano, model požádá o zavolání nástroje `create_task`. Python nástroj vykoná, vytvoří identifikátor úkolu a jeho výsledek vrátí modelu. Model následně připraví finální odpověď uživateli.

## Princip řešení

```text
E-mail
  ↓
LLM analyzuje obsah
  ↓
Rozhodnutí o použití nástroje
  ↓
Tool call create_task
  ↓
Pythonová funkce vytvoří úkol
  ↓
Výsledek nástroje se vrátí LLM
  ↓
Finální odpověď uživateli
```

Pokud e-mail pracovní požadavek neobsahuje, nástroj se nezavolá a model pouze vysvětlí důvod.

## Získávané údaje

Model z pracovního e-mailu získává:

- firmu,
- kontaktní osobu,
- název úkolu,
- stručný popis,
- termín, pokud je uveden,
- identifikátor původního e-mailu.

Argumenty nástroje jsou kontrolovány pomocí JSON schématu se zapnutým režimem `strict`.

## Simulace vytvoření úkolu

Funkce `create_task` v této výukové verzi nekomunikuje se skutečným service deskem ani databází. Vytvoření úkolu simuluje a pomocí `uuid4` mu přidělí jedinečný identifikátor ve tvaru:

```text
TASK-23F9751D
```

V reálném nasazení by funkce mohla prostřednictvím API založit úkol v externím systému a vrátit jeho skutečné ID.

## Použité technologie

- Python
- OpenAI Python SDK
- OpenAI Responses API
- model `gpt-5.4-nano`
- `python-dotenv`
- `uv`

## Instalace

Z kořenové složky repozitáře nainstalujte závislosti:

```powershell
uv sync
```

## Konfigurace API klíče

V kořenové složce projektu vytvořte soubor `.env`:

```dotenv
OPENAI_API_KEY=your_api_key_here
```

Soubor `.env` je uveden v `.gitignore` a nesmí být odeslán do veřejného repozitáře.

## Spuštění

Příkaz spusťte z kořenové složky projektu:

```powershell
uv run .\assignment_1_openai_tool_calling\main.py
```

## Pozitivní test

Testovací e-mail obsahuje žádost zákazníka o úpravu firemního webu. Model vybere nástroj `create_task`, připraví jeho argumenty a Pythonová funkce vytvoří simulovaný úkol.

Příklad výsledku:

```text
Model požádal o zavolání nástroje:
Nástroj: create_task

Výsledek Pythonové funkce:
{
  "status": "created",
  "task_id": "TASK-23F9751D"
}

Finální odpověď Mail Assistanta:
Úkol TASK-23F9751D byl vytvořen.
```

Identifikátor úkolu je při každém spuštění jiný.

## Negativní test

Při testu s e-mailem uchazečky reagující na pracovní nabídku model správně vyhodnotil, že nejde o zákaznický pracovní požadavek. Nástroj `create_task` proto nezavolal.

Příklad výsledku:

```text
Model nástroj nezavolal:
E-mail neobsahuje konkrétní pracovní požadavek.
```

## Bezpečnost

- API klíč není uložen ve zdrojovém kódu.
- Lokální `.env` je ignorován Gitem.
- Testovací e-maily a osobní údaje jsou smyšlené.
- Model smí použít pouze nástroj definovaný aplikací.

[Zpět na hlavní přehled projektu](../README.md)