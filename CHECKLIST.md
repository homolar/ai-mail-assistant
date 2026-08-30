## 1. GitHub – vlastní repozitář

- [x] Pokud ještě nemám účet, založit účet na GitHubu
- [x] Přihlásit se na GitHub
- [x] Vytvořit nový repozitář
- [x] Název nastavit například `ai-mail-assistant`
- [x] Visibility nastavit na **Public**
- [x] Nevytvářet projekt jako součást repozitáře lektora
- [x] Neklonovat repozitář lektora jako základ vlastního projektu
- [x] Pokud budu potřebovat jeho vzorový kód, zkopírovat pouze potřebné soubory nebo části kódu
- [x] Poznamenat si URL vlastního GitHub repozitáře `https://github.com/homolar/ai-mail-assistant`

## 2. OpenAI API

- [x] Přihlásit se na OpenAI API Platform
- [x] Otevřít Billing
- [x] Přidat platební kartu
- [x] Dobít malý prepaid kredit
- [x] Vypnout Auto recharge, pokud nechci automatické dobíjení
- [x] Vytvořit nový API key pro projekt
- [x] API key nikam veřejně neukládat
- [x] API key nikdy nevložit přímo do Python zdrojáku
- [x] API key nikdy necommitnout do Gitu/GitHubu

## 3. Lokální projekt

- [x] Ve VS Code vytvořit pracovní adresář `ai-mail-assistant`
- [x] V adresáři otevřít terminál
- [x] Inicializovat Python projekt pomocí `uv`
- [x] Vytvořit virtuální Python prostředí
- [x] Přidat OpenAI Python knihovnu
- [x] Přidat podporu `.env`
- [x] Vytvořit soubor `.env`
- [x] Do `.env` vložit `OPENAI_API_KEY`
- [x] Vytvořit `.env.example` bez skutečného API klíče
- [x] Vytvořit `.gitignore`
- [x] Přidat `.env` do `.gitignore`

## 4. Struktura úkolu 1

- [x] Vytvořit hlavní Python soubor, například `main.py`
- [x] Připravit testovací text pracovního e-mailu
- [x] Připojit Python aplikaci k OpenAI API
- [x] Poslat text e-mailu LLM
- [x] Definovat Python tool `create_task`
- [x] Umožnit LLM rozhodnout, zda má tool zavolat
- [x] Převzít argumenty tool callu z odpovědi LLM
- [x] Spustit Python funkci `create_task`
- [x] Vrátit výsledek funkce zpět LLM
- [x] Nechat LLM vytvořit finální odpověď uživateli
- [x] Otestovat pozitivní případ – e-mail obsahuje úkol
- [x] Otestovat negativní případ – e-mail není pracovní požadavek

## 5. Co má agent z e-mailu získat

- [x] Firma
- [x] Kontaktní osoba
- [x] Název úkolu
- [x] Stručný popis
- [x] Termín, pokud je v e-mailu uveden
- [x] Identifikátor původního e-mailu
- [x] Informaci, zda e-mail vůbec představuje pracovní úkol

## 6. Bezpečnostní kontrola před GitHubem

- [x] Zkontrolovat `.gitignore`
- [x] Zkontrolovat, že `.env` není připraven ke commitu
- [x] Prohledat zdrojáky, zda někde není skutečný API key
- [x] Do `.env.example` vložit pouze například `OPENAI_API_KEY=your_api_key_here`
- [x] Nepřidávat skutečné e-maily zákazníků
- [x] Používat pouze smyšlené testovací údaje

## 7. Git – první commit

- [x] V terminálu projektu spustit `git init`
- [x] Zkontrolovat stav pomocí `git status`
- [x] Přidat soubory pomocí `git add .`
- [x] Znovu zkontrolovat `git status`
- [x] Ověřit, že mezi soubory NENÍ `.env`
- [x] Vytvořit první commit
- [x] Commit pojmenovat například `Initialize AI Mail Assistant project`

## 8. Připojení vlastního GitHub repozitáře

- [x] Zkopírovat HTTPS adresu svého nového GitHub repozitáře
- [x] Přidat jej jako `origin`
- [x] Ověřit nastavený remote pomocí `git remote -v`
- [x] Zkontrolovat, že `origin` ukazuje na MŮJ repozitář, nikoli repozitář lektora
- [x] Nastavit hlavní větev na `main`
- [x] Provést první `git push`

## 9. README

- [x] Vytvořit `README.md`
- [x] Popsat účel projektu
- [x] Uvést, že jde o úkol č. 1 z kurzu AI agentů
- [x] Popsat princip `LLM → tool call → Python funkce → výsledek → LLM`
- [x] Přidat stručný návod instalace
- [x] Přidat stručný návod spuštění
- [x] Popsat vytvoření `.env`
- [x] Neuvádět skutečný API key
- [x] Uvést použitý model
- [x] Uvést příklad vstupu a výsledku

## 10. Finální kontrola a odevzdání

- [x] Otevřít GitHub repozitář v anonymním/private okně prohlížeče
- [x] Ověřit, že repozitář lze zobrazit bez přihlášení
- [x] Ověřit, že jsou vidět zdrojové soubory
- [x] Ověřit, že je vidět README
- [x] Ověřit, že nikde není API key
- [x] Ověřit, že `.env` není v GitHub repozitáři
- [x] Zkopírovat adresu hlavní stránky repozitáře `https://github.com/homolar/ai-mail-assistant`
- [x] Připravit odkaz k odevzdání lektorovi: `https://github.com/homolar/ai-mail-assistant/tree/main/assignment_1_openai_tool_calling`

# Úkol 2 – LangFlow agent

## 11. Příprava prostředí LangFlow

- [x] Ověřit funkční Docker Desktop
- [x] Stáhnout oficiální Docker image LangFlow
- [x] Spustit LangFlow pouze na lokální adrese `127.0.0.1:7860`
- [x] Nastavit trvalé ukládání dat do Docker volume `langflow-data`
- [x] Ověřit běžící kontejner `langflow`
- [x] Otevřít LangFlow na `http://localhost:7860`
- [x] Vytvořit flow `Mail Assistant – Assignment 2`
- [x] Připojit poskytovatele OpenAI
- [x] Nastavit OpenAI Base URL `https://api.openai.com/v1`
- [x] Povolit model `gpt-5.4-nano`
- [x] Ověřit, že API klíč není součástí Git repozitáře
- [x] Vytvořit složku `assignment_2_langflow`

## 12. Návrh řešení

- [x] Upřesnit vstup a očekávaný výstup agenta
- [x] Vytvořit základní flow v LangFlow
- [x] Přidat Chat Input
- [x] Přidat Agent
- [x] Nastavit model `gpt-5.4-nano`
- [x] Přidat Chat Output
- [x] Připravit SQLite databázi úkolů
- [x] Přidat nástroj pro zápis úkolu do databáze
- [x] Přidat nástroj pro čtení úkolů z databáze
- [x] Nastavit instrukce Mail Assistanta
- [x] Propojit komponenty flow

## 13. Testování

- [x] Otestovat vytvoření úkolu z pracovního požadavku
- [x] Ověřit uložení úkolu do databáze
- [x] Otestovat načtení uložených úkolů
- [x] Otestovat e-mail, který pracovní úkol neobsahuje
- [x] Ověřit, že agent nepoužije databázový nástroj zbytečně
- [x] Používat pouze smyšlené testovací údaje
- [x] Otestovat technické odmítnutí zakázaného příkazu `UPDATE`
- [x] Otestovat prompt injection vložený do e-mailu
- [x] Ověřit, že prompt injection nezpůsobí spuštění zakázaného SQL

## 14. Dokumentace a odevzdání

- [x] Exportovat dokončený LangFlow flow jako JSON
- [x] Uložit JSON do složky `assignment_2_langflow`
- [x] Vytvořit `assignment_2_langflow/README.md`
- [x] Popsat princip flow a použité komponenty
- [x] Přidat návod na import a spuštění
- [x] Uvést příklady testovacích vstupů a výsledků
- [x] Ověřit, že export neobsahuje API klíč
- [x] Commitnout a odeslat změny na GitHub
- [x] Ověřit veřejnou dostupnost bez přihlášení
- [x] Odevzdat přímý odkaz na složku Úkolu 2 `https://github.com/homolar/ai-mail-assistant/tree/main/assignment_2_langflow`

# Úkol 3 – Agent framework, LiteLLM a auditing

## 15. Příprava frameworku

- [x] Zvolit agentní framework OpenAI Agents SDK
- [x] Zvolit LiteLLM jako přepínač poskytovatele a modelu
- [x] Vytvořit složku `assignment_3_agent_framework`
- [x] Nainstalovat `openai-agents` s podporou LiteLLM
- [x] Ověřit kompatibilitu závislostí s Pythonem 3.14
- [x] Přidat proměnnou `LLM_MODEL` do `.env`
- [x] Přidat bezpečný příklad `LLM_MODEL` do `.env.example`
- [x] Nastavit výchozí model `openai/gpt-5.4-nano`
- [x] Vytvořit nejmenšího funkčního Agenta
- [x] Ověřit volání modelu prostřednictvím LiteLLM

## 16. Strukturovaný výstup

- [x] Vytvořit Pydantic model `AgentResponse`
- [x] Definovat povolené hodnoty `status`
- [x] Definovat povolené hodnoty `action`
- [x] Přidat volitelné `task_id`
- [x] Přidat volitelné `proposal_id`
- [x] Nastavit `output_type=AgentResponse`
- [x] Ověřit platný strukturovaný výstup
- [x] Ověřit negativní případ bez pracovního požadavku

## 17. Databáze a auditní základ

- [x] Vytvořit modul `storage.py`
- [x] Ukládat databázi do lokální složky `data`
- [x] Přidat složku `data` do `.gitignore`
- [x] Vytvořit tabulku `tasks`
- [x] Nastavit `email_id` jako unikátní hodnotu
- [x] Vytvořit tabulku `audit_events`
- [x] Vytvořit tabulku `improvement_proposals`
- [x] Inicializovat databázi při spuštění aplikace
- [x] Vytvořit funkci `record_audit_event`
- [x] Vytvořit `AppContext` s unikátním `run_id`
- [x] Předat kontext do `Runner.run_sync`
- [x] Implementovat audit začátku běhu
- [x] Implementovat audit úspěšného dokončení
- [x] Implementovat audit selhání
- [x] Ověřit záznamy `started` a `completed` přímo v databázi

## 18. Nástroje Mail Assistanta

- [x] Vytvořit frameworkový nástroj pro vytvoření úkolu
- [x] Vytvořit frameworkový nástroj pro načtení úkolů
- [x] Přidat audit každého volání nástroje
- [x] Předávat nástrojům `run_id` prostřednictvím kontextu
- [x] Zabránit duplicitnímu vytvoření úkolu podle `email_id`
- [x] Zabránit přímému spouštění libovolných SQL příkazů modelem
- [x] Připojit nástroje k Agentovi
- [x] Upravit instrukce Agenta pro bezpečné používání nástrojů

## 19. Návrhy zlepšení

- [x] Evidovat opakované typy požadavků v auditu
- [x] Vytvořit nástroj pro analýzu opakovaných požadavků
- [x] Vytvořit návrh nové schopnosti nebo nástroje
- [x] Uložit návrh do tabulky `improvement_proposals`
- [x] Nastavit nový návrh do stavu `pending`
- [x] Zabránit automatické aktivaci navrženého nástroje
- [x] Vyžadovat schválení vlastníkem nebo správcem
- [x] Ověřit, že Agent pouze předloží návrh

## 20. Bezpečnostní testy

- [x] Považovat obsah e-mailu za nedůvěryhodná data
- [x] Otestovat e-mail s prompt injection
- [x] Ověřit, že Agent neprozradí API klíč
- [x] Ověřit, že Agent nemůže měnit databázové schéma
- [x] Ověřit, že Agent nemůže mazat úkoly
- [x] Ověřit, že audit neukládá API klíč
- [x] Ověřit, že audit neukládá celé znění e-mailu
- [x] Ověřit auditní posloupnost `started → list_tasks → completed`
- [x] Používat pouze smyšlené testovací údaje

## 21. Funkční testy

- [x] Otestovat vytvoření úkolu z pracovního e-mailu
- [x] Ověřit vrácení skutečného `task_id`
- [x] Ověřit výpis uložených úkolů pomocí nástroje `list_tasks`
- [x] Ověřit strukturovanou odpověď s akcí `tasks_listed`
- [x] Otestovat e-mail bez pracovního požadavku
- [x] Otestovat opakované zpracování stejného `email_id`
- [x] Otestovat strukturovaný výstup všech hlavních větví
- [x] Otestovat změnu modelu prostřednictvím `LLM_MODEL`
- [x] Ověřit nápovědu pomocí `--help`
- [x] Otestovat zadání požadavku pomocí `--text`
- [x] Otestovat načtení e-mailu ze souboru pomocí `--file`
- [x] Ověřit srozumitelnou chybu při neexistujícím vstupním souboru

## 22. Dokumentace a odevzdání

- [x] Vytvořit `assignment_3_agent_framework/README.md`
- [x] Popsat architekturu Agenta
- [x] Popsat rozdíl mezi Agents SDK a LiteLLM
- [x] Popsat Structured Outputs
- [x] Popsat databázové nástroje
- [x] Popsat auditní stopu
- [x] Popsat schvalování návrhů zlepšení
- [x] Přidat návod instalace a spuštění
- [x] Přidat příklady vstupů a výsledků
- [x] Doplnit Úkol 3 do root `README.md`
- [x] Ověřit, že Git neobsahuje `.env` ani lokální databázi
- [x] Commitnout a odeslat změny na GitHub
- [x] Ověřit veřejnou dostupnost bez přihlášení
- [x] Odevzdat přímý odkaz na složku Úkolu 3 `https://github.com/homolar/ai-mail-assistant/tree/main/assignment_3_agent_framework`