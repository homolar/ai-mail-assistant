# AI Mail Assistant

Výukový projekt vytvořený v rámci kurzu zaměřeného na tvorbu AI agentů.

Cílem projektu je postupně vytvořit asistenta, který analyzuje pracovní e-maily, rozpozná konkrétní požadavky a pomocí nástrojů vytvoří strukturované úkoly.

## Úkol 1 – OpenAI API a tool calling

První úkol demonstruje propojení jazykového modelu s vlastní Pythonovou funkcí `create_task`.

Zdrojový kód se nachází ve složce:

```text
assignment_1_openai_tool_calling/
```

Program:

1. načte smyšlený pracovní e-mail,
2. odešle jej modelu prostřednictvím OpenAI API,
3. nechá model rozhodnout, zda e-mail obsahuje pracovní požadavek,
4. v případě požadavku zavolá Pythonovou funkci `create_task`,
5. vytvoří jedinečný identifikátor úkolu,
6. vrátí výsledek nástroje modelu,
7. zobrazí finální odpověď uživateli.

Základní tok aplikace:

```text
E-mail → LLM → tool call → Python funkce → výsledek nástroje → LLM → odpověď
```

Pokud e-mail pracovní požadavek neobsahuje, nástroj se nezavolá a model stručně vysvětlí důvod.

### Získávané údaje

Agent z e-mailu získává:

- firmu,
- kontaktní osobu,
- název úkolu,
- stručný popis,
- termín, pokud je uveden,
- identifikátor původního e-mailu.

### Použité technologie

- Python
- OpenAI Python SDK
- OpenAI Responses API
- model `gpt-5.4-nano`
- `python-dotenv`
- `uv`

### Instalace

Projekt vyžaduje nainstalovaný Python a nástroj `uv`.

Po naklonování repozitáře nainstalujte závislosti:

```powershell
uv sync
```

### Konfigurace

V kořenové složce vytvořte soubor `.env`:

```dotenv
OPENAI_API_KEY=your_api_key_here
```

Skutečný API klíč nesmí být uložen ve zdrojovém kódu ani odeslán do GitHub repozitáře. Soubor `.env` je proto uveden v `.gitignore`.

### Spuštění Úkolu 1

Z kořenové složky projektu spusťte:

```powershell
uv run .\assignment_1_openai_tool_calling\main.py
```

### Příklad výsledku

```text
Model požádal o zavolání nástroje:
Nástroj: create_task

Výsledek Pythonové funkce:
{
  "status": "created",
  "task_id": "TASK-23F9751D"
}

Finální odpověď Mail Assistanta:
Úkol byl úspěšně vytvořen.
```

## Úkol 2 – LangFlow agent s databází

Druhý úkol rozšiřuje Mail Assistanta o vizuálně sestavený agentní workflow v prostředí LangFlow.

Agent:

1. přijímá pracovní e-mail prostřednictvím Chat Input,
2. pomocí modelu `gpt-5.4-nano` rozpozná konkrétní pracovní požadavek,
3. vytvoří úkol v SQLite databázi pomocí SQL nástroje,
4. umožňuje uložené úkoly vyhledávat a vypisovat,
5. odmítá e-maily, které pracovní požadavek neobsahují,
6. považuje obsah e-mailu za nedůvěryhodná data,
7. technicky omezuje SQL nástroj pouze na bezpečné operace `SELECT` a `INSERT`.

Exportovaný LangFlow workflow a podrobná dokumentace jsou ve složce:

```text
assignment_2_langflow/
├── mail_assistant_langflow.json
└── README.md
```
Podrobný popis, postup importu, databázové schéma a testovací scénáře jsou uvedeny v [README Úkolu 2](assignment_2_langflow/README.md).

## Úkol 3 – Mail Assistant s OpenAI Agents SDK

Třetí úkol navazuje na předchozí řešení a vytváří samostatnou Pythonovou aplikaci založenou na frameworku OpenAI Agents SDK.

Agent:

1. přijímá e-mail nebo požadavek z příkazové řádky či textového souboru,
2. rozpoznává konkrétní pracovní požadavky a vytváří úkoly v SQLite databázi,
3. zabraňuje duplicitnímu vytvoření úkolu podle `email_id`,
4. umožňuje uložené úkoly vypisovat,
5. u neúplného požadavku žádá o doplnění informací,
6. vrací strukturovanou odpověď podle Pydantic schématu,
7. používá LiteLLM pro konfiguraci modelu bez změny zdrojového kódu,
8. zaznamenává běhy a volání nástrojů do lokálního auditu,
9. na výslovnou žádost analyzuje opakované kategorie požadavků,
10. vytváří návrhy zlepšení ve stavu `pending`, bez jejich automatické implementace nebo aktivace.

### Struktura řešení

```text
assignment_3_agent_framework/
├── main.py
├── tools.py
├── storage.py
├── app_context.py
├── examples/
│   └── email_incomplete.txt
└── README.md
```

Lokální databáze vzniká automaticky ve složce `data/`, která není součástí Git repozitáře.

### Použité technologie

- Python 3.14 nebo novější
- OpenAI Agents SDK
- LiteLLM
- Pydantic
- SQLite
- `python-dotenv`
- `argparse`
- `uv`

OpenAI Agents SDK řídí běh Agenta a volání nástrojů. LiteLLM zajišťuje připojení nakonfigurovaného modelu. Pydantic definuje strukturu finální odpovědi.

### Konfigurace a spuštění

Z kořene repozitáře nainstalujte závislosti:

```powershell
uv sync --locked
```

Do lokálního souboru `.env` doplňte:

```dotenv
OPENAI_API_KEY=your_api_key_here
LLM_MODEL=openai/gpt-5.4-nano
```

Výpis uložených úkolů:

```powershell
uv run .\assignment_3_agent_framework\main.py --text "Vypiš všechny úkoly uložené v DB."
```

Zpracování ukázkového neúplného e-mailu:

```powershell
uv run .\assignment_3_agent_framework\main.py --file .\assignment_3_agent_framework\examples\email_incomplete.txt
```

Analýza opakovaných požadavků:

```powershell
uv run .\assignment_3_agent_framework\main.py --text "Analyzuj opakované typy požadavků a případně navrhni zlepšení."
```

### Audit a návrhy zlepšení

Audit propojuje jednotlivé události pomocí `run_id` a zaznamenává také zvolený model, použité nástroje a výsledky operací.

Příklad průběhu:

```text
started → create_task → completed
```

Vlastní lokální audit neukládá API klíče ani celé texty e-mailů.

Při alespoň třech úspěšně vytvořených úkolech stejné kategorie může analýza navrhnout specializovaný nástroj. Jde o jednoduché vyhodnocení četnosti, nikoliv o automatické trénování modelu.

Návrh čeká na posouzení člověkem. Schvalovací rozhraní, implementace a nasazování nových nástrojů nejsou součástí školní verze.

### Rozsah školní verze

Aplikace pracuje s lokálními textovými vstupy a SQLite databází. Není připojena ke skutečné e-mailové schránce ani externímu správci úkolů.

Model má dostupné pouze předem definované nástroje, nikoliv libovolné SQL nebo systémové příkazy. Řešení je výukovým základem pro další rozvoj, nikoliv hotovou produkční službou.

Podrobný popis architektury, instalace, testů a omezení je uveden v [README Úkolu 3](assignment_3_agent_framework/README.md).

Použité e-maily a zákaznické údaje jsou smyšlené a slouží pouze k výukovým účelům.