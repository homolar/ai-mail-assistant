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

Použité e-maily a zákaznické údaje jsou smyšlené a slouží pouze k výukovým účelům.