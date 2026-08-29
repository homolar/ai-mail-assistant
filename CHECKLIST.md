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

- [ ] Otevřít GitHub repozitář v anonymním/private okně prohlížeče
- [ ] Ověřit, že repozitář lze zobrazit bez přihlášení
- [ ] Ověřit, že jsou vidět zdrojové soubory
- [ ] Ověřit, že je vidět README
- [ ] Ověřit, že nikde není API key
- [x] Ověřit, že `.env` není v GitHub repozitáři
- [ ] Zkopírovat adresu hlavní stránky repozitáře
- [ ] Tento odkaz odevzdat lektorovi