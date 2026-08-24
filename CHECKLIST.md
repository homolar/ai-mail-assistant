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

- [ ] Přihlásit se na OpenAI API Platform
- [ ] Otevřít Billing
- [ ] Přidat platební kartu
- [ ] Dobít malý prepaid kredit
- [ ] Vypnout Auto recharge, pokud nechci automatické dobíjení
- [ ] Vytvořit nový API key pro projekt
- [ ] API key nikam veřejně neukládat
- [ ] API key nikdy nevložit přímo do Python zdrojáku
- [ ] API key nikdy necommitnout do Gitu/GitHubu

## 3. Lokální projekt

- [x] Ve VS Code vytvořit pracovní adresář `ai-mail-assistant`
- [x] V adresáři otevřít terminál
- [x] Inicializovat Python projekt pomocí `uv`
- [x] Vytvořit virtuální Python prostředí
- [x] Přidat OpenAI Python knihovnu
- [ ] Přidat podporu `.env`
- [x] Vytvořit soubor `.env`
- [ ] Do `.env` vložit `OPENAI_API_KEY`
- [x] Vytvořit `.env.example` bez skutečného API klíče
- [x] Vytvořit `.gitignore`
- [x] Přidat `.env` do `.gitignore`

## 4. Struktura úkolu 1

- [x] Vytvořit hlavní Python soubor, například `main.py`
- [ ] Připravit testovací text pracovního e-mailu
- [ ] Připojit Python aplikaci k OpenAI API
- [ ] Poslat text e-mailu LLM
- [ ] Definovat Python tool `create_task`
- [ ] Umožnit LLM rozhodnout, zda má tool zavolat
- [ ] Převzít argumenty tool callu z odpovědi LLM
- [ ] Spustit Python funkci `create_task`
- [ ] Vrátit výsledek funkce zpět LLM
- [ ] Nechat LLM vytvořit finální odpověď uživateli
- [ ] Otestovat pozitivní případ – e-mail obsahuje úkol
- [ ] Otestovat negativní případ – e-mail není pracovní požadavek

## 5. Co má agent z e-mailu získat

- [ ] Firma
- [ ] Kontaktní osoba
- [ ] Název úkolu
- [ ] Stručný popis
- [ ] Termín, pokud je v e-mailu uveden
- [ ] Identifikátor původního e-mailu
- [ ] Informaci, zda e-mail vůbec představuje pracovní úkol

## 6. Bezpečnostní kontrola před GitHubem

- [ ] Zkontrolovat `.gitignore`
- [ ] Zkontrolovat, že `.env` není připraven ke commitu
- [ ] Prohledat zdrojáky, zda někde není skutečný API key
- [ ] Do `.env.example` vložit pouze například `OPENAI_API_KEY=your_api_key_here`
- [ ] Nepřidávat skutečné e-maily zákazníků
- [ ] Používat pouze smyšlené testovací údaje

## 7. Git – první commit

- [ ] V terminálu projektu spustit `git init`
- [ ] Zkontrolovat stav pomocí `git status`
- [ ] Přidat soubory pomocí `git add .`
- [ ] Znovu zkontrolovat `git status`
- [ ] Ověřit, že mezi soubory NENÍ `.env`
- [ ] Vytvořit první commit
- [ ] Commit pojmenovat například `Initial version of LLM tool calling assignment`

## 8. Připojení vlastního GitHub repozitáře

- [ ] Zkopírovat HTTPS adresu svého nového GitHub repozitáře
- [ ] Přidat jej jako `origin`
- [ ] Ověřit nastavený remote pomocí `git remote -v`
- [ ] Zkontrolovat, že `origin` ukazuje na MŮJ repozitář, nikoli repozitář lektora
- [ ] Nastavit hlavní větev na `main`
- [ ] Provést první `git push`

## 9. README

- [ ] Vytvořit `README.md`
- [ ] Popsat účel projektu
- [ ] Uvést, že jde o úkol č. 1 z kurzu AI agentů
- [ ] Popsat princip `LLM → tool call → Python funkce → výsledek → LLM`
- [ ] Přidat stručný návod instalace
- [ ] Přidat stručný návod spuštění
- [ ] Popsat vytvoření `.env`
- [ ] Neuvádět skutečný API key
- [ ] Uvést použitý model
- [ ] Uvést příklad vstupu a výsledku

## 10. Finální kontrola a odevzdání

- [ ] Otevřít GitHub repozitář v anonymním/private okně prohlížeče
- [ ] Ověřit, že repozitář lze zobrazit bez přihlášení
- [ ] Ověřit, že jsou vidět zdrojové soubory
- [ ] Ověřit, že je vidět README
- [ ] Ověřit, že nikde není API key
- [ ] Ověřit, že `.env` není v GitHub repozitáři
- [ ] Zkopírovat adresu hlavní stránky repozitáře
- [ ] Tento odkaz odevzdat lektorovi