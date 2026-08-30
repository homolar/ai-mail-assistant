# Úkol 3 – Mail Assistant s OpenAI Agents SDK

Tento úkol demonstruje vytvoření AI agenta pomocí frameworku OpenAI Agents SDK.

Agent zpracovává pracovní e-maily, ukládá konkrétní požadavky jako úkoly do SQLite databáze a umožňuje jejich výpis. Používá strukturované odpovědi, přepínání modelu prostřednictvím LiteLLM a vlastní lokální audit.

Na základě opakovaných kategorií požadavků dokáže vytvořit návrh zlepšení. Návrh pouze uloží ke schválení – žádný nový nástroj automaticky nevytváří ani neaktivuje.

## Princip řešení

```text
E-mail nebo požadavek z příkazové řádky či souboru
  ↓
Kontrola vstupu a zahájení auditu
  ↓
Agent řízený OpenAI Agents SDK
  ↓
Model připojený prostřednictvím LiteLLM
  ↓
Rozhodnutí o použití povoleného nástroje
  ↓
Pythonová funkce a SQLite databáze
  ↓
Výsledek nástroje se vrátí Agentovi
  ↓
Strukturovaná odpověď podle Pydantic schématu
  ↓
Dokončení auditu a výpis JSON
```

Pokud e-mail neobsahuje pracovní požadavek, Agent jej zamítne bez vytvoření úkolu. Pokud pracovní požadavek naznačuje, ale chybí zásadní informace, Agent požádá o jejich doplnění.

## Použité technologie

- Python 3.14 nebo novější
- OpenAI Agents SDK
- LiteLLM
- model `openai/gpt-5.4-nano`
- Pydantic
- SQLite
- `python-dotenv`
- `argparse`
- `uv`

Konkrétní verze závislostí jsou zachyceny v souboru `uv.lock` v kořeni repozitáře.

## Struktura řešení

- `main.py` – načtení vstupu, konfigurace Agenta, struktura odpovědi a řízení běhu.
- `tools.py` – nástroje pro vytváření úkolů, jejich výpis a analýzu auditu.
- `storage.py` – správa SQLite připojení, inicializace tabulek a ukládání auditu.
- `app_context.py` – lokální kontext s identifikátorem běhu a uživatele.
- `examples/email_incomplete.txt` – smyšlený neúplný e-mail pro test načítání ze souboru.
- `data/mail_assistant.db` – lokální databáze vytvářená při spuštění; není součástí repozitáře.

## OpenAI Agents SDK a LiteLLM

OpenAI Agents SDK v této aplikaci řídí běh Agenta: předává instrukce modelu, zpracovává volání nástrojů a poskytuje finální odpověď.

LiteLLM slouží jako vrstva pro připojení modelu. Jeho název je načítán z proměnné `LLM_MODEL`, takže pro změnu konfigurace modelu není nutné upravovat Pythonový kód.

Použitý formát:

```text
poskytovatel/model
```

Výchozí konfigurace:

```dotenv
LLM_MODEL=openai/gpt-5.4-nano
```

Přechod k jinému poskytovateli vyžaduje také odpovídající přihlašovací údaje a ověření podpory nástrojů a strukturovaného výstupu. Samotná změna názvu není zárukou kompatibility.

## Strukturované odpovědi

Finální odpověď je definována Pydantic modelem `AgentResponse`, který je předán Agentovi prostřednictvím `output_type`.

Nejde pouze o textovou instrukci „odpovídej v JSON“. Aplikace používá výstupní schéma a validaci výsledku.

Odpověď obsahuje:

- `status` – výsledek zpracování,
- `action` – provedenou akci,
- `message` – zprávu pro uživatele,
- `task_id` – identifikátor úkolu, pokud je relevantní,
- `proposal_id` – identifikátor návrhu zlepšení, pokud je relevantní,
- `tasks` – seznam úkolů při výpisu.

Příklad odpovědi při neúplném požadavku:

```json
{
  "status": "needs_clarification",
  "action": "no_action",
  "message": "Prosím doplňte, které stránky a jak konkrétně potřebujete upravit.",
  "task_id": null,
  "proposal_id": null,
  "tasks": []
}
```

Schéma kontroluje strukturu odpovědi, nikoliv pravdivost jejího obsahu. Technická chyba nebo odmítnutí na straně poskytovatele mohou běh přerušit; nelze tedy předpokládat úspěšnou odpověď za všech okolností.

Více informací: [OpenAI Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs).

## Databázové nástroje

### create_task

Vytvoří úkol z konkrétního pracovního požadavku.

Ukládá zejména:

- identifikátor e-mailu,
- firmu,
- kontaktní osobu,
- název a popis úkolu,
- termín,
- stav úkolu.

Kategorie požadavku se zaznamenává do auditu pro následnou analýzu.

Nástroj kontroluje datum a používá parametrizované SQL. Unikátní hodnota `email_id` chrání před opakovaným vytvořením úkolu ze stejného e-mailu.

Při duplicitě vrátí identifikátor existujícího úkolu.

### list_tasks

Načítá úkoly z databáze.

Podporuje filtr podle stavu a omezuje velikost výsledku na nejvýše 50 záznamů. Výchozí limit je 10, takže výpis není neomezený.

Model nepředává vlastní SQL příkaz. Volí pouze parametry připravené Pythonové funkce.

### analyze_repeated_requests

Vyhodnocuje kategorie úspěšně vytvořených úkolů podle lokálního auditu.

Pokud nejčastější kategorie obsahuje alespoň tři výskyty, vytvoří návrh specializovaného nástroje. Pokud již stejný návrh čeká na schválení, vrátí existující záznam.

Analýza se spouští na výslovný požadavek uživatele, nikoliv automaticky po každém e-mailu.

## Databáze

Databáze je uložena v souboru:

```text
assignment_3_agent_framework/data/mail_assistant.db
```

Obsahuje tabulky:

- `tasks` – uložené úkoly,
- `audit_events` – auditní události,
- `improvement_proposals` – návrhy zlepšení.

Složka a tabulky vzniknou automaticky při prvním běhu s platným vstupem. Docker není pro Úkol 3 potřeba.

Databáze ani testovací záznamy nejsou součástí Git repozitáře. Nová instalace proto začíná s prázdnými tabulkami.

## Auditní stopa

Každý běh má vlastní `run_id`, který propojuje jeho auditní události.

Příklad úspěšného vytvoření úkolu:

```text
started → create_task → completed
```

Příklad požadavku na doplnění informací:

```text
started → completed
```

Audit zachycuje například:

- identifikátor běhu,
- použitou konfiguraci modelu,
- název nástroje a identifikátor jeho volání,
- úspěch nebo neúspěch operace,
- kategorii požadavku,
- identifikátor úkolu nebo návrhu,
- počet nalezených výsledků.

Vlastní lokální audit neukládá API klíče ani celé texty e-mailů. Popis úkolu a kontaktní údaje se však ukládají do tabulky `tasks`.

Lokální audit není totéž jako případné trasování a telemetrie použitých knihoven nebo poskytovatele. Před produkčním použitím je nutné samostatně posoudit i tyto datové toky.

## Návrhy zlepšení a schvalování

Ověřený scénář:

1. Agent vytvoří tři různé úkoly kategorie `website`.
2. Uživatel požádá o analýzu opakovaných požadavků.
3. Nástroj vytvoří návrh `specialized_website_tool`.
4. Návrh má stav `pending` a `approved_at` zůstává prázdné.
5. Opakovaná analýza vrátí stejný čekající návrh bez vytvoření duplicity.

Jde o jednoduché pravidlo nad četností kategorií, nikoliv o trénování modelu nebo důkaz ekonomické výhodnosti nového nástroje.

Školní verze neimplementuje schvalovací rozhraní ani nasazení navržených nástrojů. Posouzení, schválení a případná implementace zůstávají na vlastníkovi nebo správci procesu.

## Instalace

Předpokladem je dostupné `uv` a OpenAI API účet s kreditem.

Z kořenové složky repozitáře spusťte:

```powershell
uv sync --locked
```

Závislosti se nainstalují podle společného `pyproject.toml` a `uv.lock`.

## Konfigurace

V kořenové složce repozitáře vytvořte `.env` podle `.env.example`:

```dotenv
OPENAI_API_KEY=your_api_key_here
LLM_MODEL=openai/gpt-5.4-nano
```

Pokud `.env` již používáte pro předchozí úkoly, doplňte pouze chybějící hodnoty.

Soubor `.env` je ignorován Gitem a nesmí být publikován. API volání spotřebovávají kredit poskytovatele.

## Spuštění

Všechny následující příkazy spouštějte z kořene repozitáře.

### Nápověda

```powershell
uv run .\assignment_3_agent_framework\main.py --help
```

Nápověda nevolá model.

### Krátký textový požadavek

```powershell
uv run .\assignment_3_agent_framework\main.py --text "Vypiš všechny úkoly uložené v DB."
```

Na nové instalaci bude seznam úkolů prázdný.

### E-mail ze souboru

```powershell
uv run .\assignment_3_agent_framework\main.py --file .\assignment_3_agent_framework\examples\email_incomplete.txt
```

Ukázkový e-mail záměrně neobsahuje konkrétní rozsah práce. Očekávaný výsledek je `needs_clarification` bez vytvoření úkolu.

Soubor musí obsahovat obyčejný text v UTF-8; podporováno je také UTF-8 s BOM. Parametr `--file` není parserem exportů `.eml`, HTML ani příloh.

Je nutné zadat právě jeden parametr: `--text` nebo `--file`. Prázdný vstup, neexistující soubor či nečitelné kódování se odmítnou před API voláním.

## Pozitivní test a duplicita

Vytvoření úkolu lze vyzkoušet tímto smyšleným vstupem:

```powershell
uv run .\assignment_3_agent_framework\main.py --text "ID e-mailu: DEMO-001. Firma: Demo Web s.r.o. Kontaktní osoba: Jana Testovací. Prosím doplňte na firemní web stránku s přehledem služeb do 30. září 2026."
```

Očekávaný výsledek prvního zpracování:

```json
{
  "status": "success",
  "action": "task_created",
  "message": "Úkol byl vytvořen.",
  "task_id": 1,
  "proposal_id": null,
  "tasks": []
}
```

Konkrétní ID závisí na obsahu databáze a formulace zprávy se může lišit.

Při opakování stejného příkazu očekáváme `task_duplicate` a původní identifikátor úkolu.

## Analýza opakovaných požadavků

```powershell
uv run .\assignment_3_agent_framework\main.py --text "Analyzuj opakované typy požadavků a případně navrhni zlepšení."
```

Pokud není dostatek záznamů, Agent vrátí `success` a `no_action` s vysvětlením.

Pro test vytvoření návrhu nejprve zpracujte alespoň tři různé e-maily stejné kategorie s unikátními `email_id`. Opakované spuštění stejného e-mailu se nezapočítává jako další úspěšně vytvořený úkol.

Při vytvoření návrhu Agent vrátí `improvement_proposed` a jeho `proposal_id`.

## Ověřené scénáře

Během vývoje byly ručně ověřeny:

- vytvoření úkolu a vrácení skutečného databázového ID,
- opakované zpracování stejného e-mailu bez duplicity,
- načtení uložených úkolů,
- zamítnutí nepracovního e-mailu,
- požadavek na doplnění neúplného zadání,
- strukturované odpovědi hlavních aplikačních větví,
- návaznost běhu a nástrojových volání v auditu,
- nedostatek důkazů pro návrh zlepšení,
- vytvoření čekajícího návrhu ze tří požadavků,
- opakovaná analýza bez duplicity návrhu,
- ignorování testovací prompt injection,
- vstupy `--text`, `--file` a nápověda `--help`,
- odmítnutí neexistujícího souboru.

Bylo také ověřeno přepnutí konfigurace z `openai/gpt-5.4-nano` na `openai/gpt-5.4-nano-2026-03-17` bez změny kódu a zaznamenání zvolené hodnoty v auditu. Tento test ověřuje změnu identifikátoru modelu, nikoliv přechod k jinému poskytovateli; alias může odkazovat na stejnou verzi modelu.

## Bezpečnost a omezení

- Model nemá nástroj pro spouštění libovolného SQL, příkazů systému ani čtení konfigurace.
- Databázové operace jsou definovány v Pythonu a používají parametrizované SQL.
- Agent nemá vystavený nástroj pro mazání úkolů nebo změnu databázového schématu.
- Obsah e-mailů je v instrukcích označen jako nedůvěryhodný.
- Úspěšný test prompt injection není zárukou odolnosti proti všem útokům.
- API klíče a lokální databáze nejsou určeny k publikování.
- Text vstupu se předává zvolenému poskytovateli modelu; používejte pouze data, která mu smíte odeslat.
- Aplikace nemá přístup ke skutečné schránce a neodesílá e-maily.
- Neobsahuje integraci se skutečným správcem úkolů ani produkční sandbox.
- Audit není neměnný bezpečnostní log a aplikace není určena pro souběžný víceuživatelský provoz.
- Technická chyba může ukončit běh výjimkou namísto finální JSON odpovědi.

Řešení je výukový základ pro další rozvoj Mail Assistanta, nikoliv hotová produkční služba.

[Zpět na hlavní přehled projektu](../README.md)