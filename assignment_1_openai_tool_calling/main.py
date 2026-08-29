# Import knihovny json
import json

from dotenv import load_dotenv
from openai import OpenAI
from uuid import uuid4


# Smyšlený e-mail použitý pro pozitivní test.
TEST_EMAIL = """
ID e-mailu: EMAIL-2026-001
Od: Jana Nováková <jana.novakova@acme-example.cz>
Firma: ACME s.r.o.
Předmět: Úprava firemního webu

Dobrý den,

potřebovali bychom na našem firemním webu doplnit novou stránku
s přehledem služeb a kontaktním formulářem. Bylo by možné návrh
připravit do 15. září 2026?

Děkuji
Jana Nováková
"""


# Simulace vytvoření úkolu v externím service desku.
def create_task(
    company: str,
    contact_person: str,
    title: str,
    description: str,
    deadline: str | None,
    email_id: str,
):
    """Později zde úkol skutečně uložíme."""
    return {
        "status": "created",
        "task_id": f"TASK-{uuid4().hex[:8].upper()}",
        "company": company,
        "contact_person": contact_person,
        "title": title,
        "description": description,
        "deadline": deadline,
        "email_id": email_id,
    }


# JSON schéma nástroje, které modelu popisuje povolené argumenty.
TOOLS = [
    {
        "type": "function",
        "name": "create_task",
        "description": (
            "Vytvoří pracovní úkol z e-mailu. Použij tento nástroj pouze tehdy, "
            "když e-mail skutečně obsahuje pracovní požadavek."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "company": {
                    "type": "string",
                    "description": "Firma, která požadavek poslala.",
                },
                "contact_person": {
                    "type": "string",
                    "description": "Jméno kontaktní osoby.",
                },
                "title": {
                    "type": "string",
                    "description": "Krátký název úkolu.",
                },
                "description": {
                    "type": "string",
                    "description": "Stručný popis požadované práce.",
                },
                "deadline": {
                    "type": ["string", "null"],
                    "description": "Termín ve formátu YYYY-MM-DD, nebo null.",
                },
                "email_id": {
                    "type": "string",
                    "description": "Identifikátor původního e-mailu.",
                },
            },
            "required": [
                "company",
                "contact_person",
                "title",
                "description",
                "deadline",
                "email_id",
            ],
            "additionalProperties": False,
        },
        "strict": True,
    }
]


def main():
    load_dotenv()
    client = OpenAI()

    # První volání: model analyzuje e-mail a rozhodne, zda použije nástroj.
    response = client.responses.create(
        model="gpt-5.4-nano",
        instructions=(
            "Jsi asistent pro zpracování pracovních e-mailů. "
            "Pokud e-mail obsahuje konkrétní pracovní požadavek, "
            "použij nástroj create_task. Jinak pouze stručně vysvětli, "
            "že e-mail neobsahuje úkol."
        ),
        input=TEST_EMAIL,
        tools=TOOLS,
        tool_choice="auto",
        parallel_tool_calls=False,
    )

    for item in response.output:
        if item.type == "function_call":
            arguments = json.loads(item.arguments)

            print("Model požádal o zavolání nástroje:")
            print("Nástroj:", item.name)
            print("Argumenty:")
            print(json.dumps(arguments, indent=2, ensure_ascii=False))

            if item.name != "create_task":
                raise ValueError(f"Neznámý nástroj: {item.name}")

            # Python vykoná nástroj požadovaný modelem.
            tool_result = create_task(**arguments)

            print("\nVýsledek Pythonové funkce:")
            print(json.dumps(tool_result, indent=2, ensure_ascii=False))

            # Druhé volání: výsledek nástroje se vrátí modelu pro finální odpověď.
            final_response = client.responses.create(
                model="gpt-5.4-nano",
                previous_response_id=response.id,
                instructions=(
                    "Na základě výsledku nástroje stručně česky potvrď, "
                    "že byl úkol vytvořen. Uveď jeho task_id, název a termín."
                ),
                input=[
                    {
                        "type": "function_call_output",
                        "call_id": item.call_id,
                        "output": json.dumps(tool_result, ensure_ascii=False),
                    }
                ],
            )

            print("\nFinální odpověď Mail Assistanta:")
            print(final_response.output_text)
            return

    # Pokud model nástroj nevybral, zobrazíme jeho vysvětlení.
    print("Model nástroj nezavolal:")
    print(response.output_text)


if __name__ == "__main__":
    main()