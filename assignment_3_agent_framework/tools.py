import json
from collections import Counter
from datetime import date
from typing import Annotated, Literal

from agents import function_tool
from agents.tool_context import ToolContext

from app_context import AppContext
from storage import get_connection, record_audit_event


# Omezený výčet kategorií se promítne do JSON schématu nástroje.
# Model proto nemůže vrátit libovolný název kategorie.
TaskCategory = Literal[
    "website",
    "support",
    "billing",
    "sales",
    "administration",
    "other",
]


# Dekorátor převede Pythonovou funkci, její typy a docstring
# na nástroj, který může Agents SDK nabídnout jazykovému modelu.
@function_tool
def create_task(
    ctx: ToolContext[AppContext],
    email_id: Annotated[str, "Unique identifier of the source email"],
    title: Annotated[str, "Short and specific task title"],
    description: Annotated[str, "Description of the requested work"],
    category: Annotated[TaskCategory, "Category of the request"],
    company: Annotated[str | None, "Company name if present"] = None,
    contact_person: Annotated[str | None, "Contact person if present"] = None,
    deadline: Annotated[
        str | None,
        "Deadline in YYYY-MM-DD format if present",
    ] = None,
) -> dict:
    """Create one task from a concrete work request."""

    # ToolContext neposílá modelu interní kontext jako argument.
    # Framework jej doplní sám a poskytne run_id i metadata tool callu.

    # Datum validujeme v Pythonu ještě před zápisem do databáze.
    if deadline is not None:
        try:
            date.fromisoformat(deadline)
        except ValueError:
            record_audit_event(
                run_id=ctx.context.run_id,
                event_type="tool_call",
                action="create_task",
                tool_name=ctx.tool_name,
                success=False,
                details={
                    "tool_call_id": ctx.tool_call_id,
                    "result": "invalid_deadline",
                    "category": category,
                },
            )
            return {
                "status": "error",
                "error": "Deadline must use YYYY-MM-DD format.",
            }

    try:
        with get_connection() as connection:
            # email_id funguje jako idempotency key:
            # opakované zpracování stejného e-mailu nevytvoří duplicitu.
            existing = connection.execute(
                """
                SELECT id, title, status
                FROM tasks
                WHERE email_id = ?
                """,
                (email_id,),
            ).fetchone()

            if existing is not None:
                record_audit_event(
                    run_id=ctx.context.run_id,
                    event_type="tool_call",
                    action="create_task",
                    tool_name=ctx.tool_name,
                    success=False,
                    details={
                        "tool_call_id": ctx.tool_call_id,
                        "result": "duplicate",
                        "category": category,
                        "task_id": existing["id"],
                    },
                )
                return {
                    "status": "duplicate",
                    "task": dict(existing),
                }

            # Parametrizovaný SQL dotaz odděluje data od SQL příkazu
            # a brání vložení SQL kódu prostřednictvím obsahu e-mailu.
            cursor = connection.execute(
                """
                INSERT INTO tasks (
                    email_id,
                    company,
                    contact_person,
                    title,
                    description,
                    deadline
                )
                VALUES (?, ?, ?, ?, ?, ?)
                """,
                (
                    email_id,
                    company,
                    contact_person,
                    title,
                    description,
                    deadline,
                ),
            )

            task_id = int(cursor.lastrowid)

        # Audit ukládá pouze metadata nutná pro dohledání činnosti.
        # Celé znění e-mailu ani popis úkolu se do auditu nekopírují.
        record_audit_event(
            run_id=ctx.context.run_id,
            event_type="tool_call",
            action="create_task",
            tool_name=ctx.tool_name,
            success=True,
            details={
                "tool_call_id": ctx.tool_call_id,
                "result": "created",
                "category": category,
                "task_id": task_id,
            },
        )

        return {
            "status": "created",
            "task_id": task_id,
            "email_id": email_id,
            "title": title,
            "deadline": deadline,
            "task_status": "new",
        }

    # Uživateli vracíme obecnou chybu, zatímco audit uchová pouze její typ.
    # Interní databázové detaily tak zbytečně neuniknou modelu.
    except Exception as error:
        record_audit_event(
            run_id=ctx.context.run_id,
            event_type="tool_call",
            action="create_task",
            tool_name=ctx.tool_name,
            success=False,
            details={
                "tool_call_id": ctx.tool_call_id,
                "result": "error",
                "error_type": type(error).__name__,
                "category": category,
            },
        )
        return {
            "status": "error",
            "error": "Task could not be created.",
        }


@function_tool
def list_tasks(
    ctx: ToolContext[AppContext],
    status: Annotated[
        Literal["all", "new", "completed"],
        "Filter tasks by status",
    ] = "all",
    limit: Annotated[int, "Maximum number of returned tasks from 1 to 50"] = 10,
) -> dict:
    """List tasks stored in the local database."""

    # Pevný rozsah chrání databázi před neomezeně velkým výsledkem.
    safe_limit = max(1, min(limit, 50))

    try:
        with get_connection() as connection:
            # Model neovládá SQL text. Volí pouze z předem připravených větví.
            if status == "all":
                rows = connection.execute(
                    """
                    SELECT id, email_id, company, title, deadline, status, created_at
                    FROM tasks
                    ORDER BY id DESC
                    LIMIT ?
                    """,
                    (safe_limit,),
                ).fetchall()
            else:
                rows = connection.execute(
                    """
                    SELECT id, email_id, company, title, deadline, status, created_at
                    FROM tasks
                    WHERE status = ?
                    ORDER BY id DESC
                    LIMIT ?
                    """,
                    (status, safe_limit),
                ).fetchall()

        tasks = [dict(row) for row in rows]

        record_audit_event(
            run_id=ctx.context.run_id,
            event_type="tool_call",
            action="list_tasks",
            tool_name=ctx.tool_name,
            success=True,
            details={
                "tool_call_id": ctx.tool_call_id,
                "status_filter": status,
                "result_count": len(tasks),
            },
        )

        return {
            "status": "success",
            "count": len(tasks),
            "tasks": tasks,
        }

    except Exception as error:
        record_audit_event(
            run_id=ctx.context.run_id,
            event_type="tool_call",
            action="list_tasks",
            tool_name=ctx.tool_name,
            success=False,
            details={
                "tool_call_id": ctx.tool_call_id,
                "status_filter": status,
                "error_type": type(error).__name__,
            },
        )
        return {
            "status": "error",
            "error": "Tasks could not be loaded.",
        }


@function_tool
def analyze_repeated_requests(
    ctx: ToolContext[AppContext],
) -> dict:
    """Analyze audit metadata and propose a capability for repeated requests."""

    # Návrh vznikne až po třech úspěšných požadavcích stejné kategorie.
    # Jednorázový výskyt proto není považován za opakující se potřebu.
    minimum_evidence = 3

    try:
        with get_connection() as connection:
            # Analyzujeme pouze metadata úspěšně vytvořených úkolů.
            # Celé texty e-mailů nejsou pro analýzu potřeba.
            rows = connection.execute(
                """
                SELECT details_json
                FROM audit_events
                WHERE action = 'create_task'
                  AND success = 1
                """
            ).fetchall()

            # Kategorie jsou bezpečně načteny z JSON části auditních záznamů.
            categories: list[str] = []

            for row in rows:
                details = json.loads(row["details_json"])
                category = details.get("category")

                if isinstance(category, str):
                    categories.append(category)

            # Counter spočítá výskyty jednotlivých kategorií požadavků.
            category_counts = Counter(categories)

            if not category_counts:
                result = {
                    "status": "insufficient_evidence",
                    "message": "No successful categorized requests were found.",
                    "evidence_count": 0,
                }
            else:
                category, evidence_count = category_counts.most_common(1)[0]

                if evidence_count < minimum_evidence:
                    result = {
                        "status": "insufficient_evidence",
                        "category": category,
                        "evidence_count": evidence_count,
                        "required_count": minimum_evidence,
                    }
                else:
                    capability = f"specialized_{category}_tool"

                    # Před vytvořením návrhu ověříme, zda stejný návrh
                    # již nečeká na schválení vlastníkem nebo správcem.
                    existing = connection.execute(
                        """
                        SELECT id, capability, reason, evidence_count, status
                        FROM improvement_proposals
                        WHERE capability = ?
                          AND status = 'pending'
                        ORDER BY id DESC
                        LIMIT 1
                        """,
                        (capability,),
                    ).fetchone()

                    if existing is not None:
                        result = {
                            "status": "already_proposed",
                            "proposal_id": existing["id"],
                            "capability": existing["capability"],
                            "evidence_count": existing["evidence_count"],
                            "proposal_status": existing["status"],
                            "requires_approval": True,
                            "activated": False,
                        }
                    else:
                        reason = (
                            f"Category '{category}' appeared in "
                            f"{evidence_count} successful task requests."
                        )

                        # Agent pouze uloží návrh ve stavu pending.
                        # Nevytváří ani neaktivuje žádný spustitelný nástroj.
                        cursor = connection.execute(
                            """
                            INSERT INTO improvement_proposals (
                                capability,
                                reason,
                                evidence_count,
                                status
                            )
                            VALUES (?, ?, ?, 'pending')
                            """,
                            (capability, reason, evidence_count),
                        )

                        proposal_id = int(cursor.lastrowid)

                        result = {
                            "status": "proposed",
                            "proposal_id": proposal_id,
                            "capability": capability,
                            "category": category,
                            "evidence_count": evidence_count,
                            "proposal_status": "pending",
                            "requires_approval": True,
                            "activated": False,
                        }

        # Také samotná analýza a případné vytvoření návrhu mají auditní stopu.
        record_audit_event(
            run_id=ctx.context.run_id,
            event_type="tool_call",
            action="analyze_repeated_requests",
            tool_name=ctx.tool_name,
            success=True,
            details={
                "tool_call_id": ctx.tool_call_id,
                "result": result["status"],
                "evidence_count": result.get("evidence_count", 0),
                "proposal_id": result.get("proposal_id"),
            },
        )

        return result

    except Exception as error:
        record_audit_event(
            run_id=ctx.context.run_id,
            event_type="tool_call",
            action="analyze_repeated_requests",
            tool_name=ctx.tool_name,
            success=False,
            details={
                "tool_call_id": ctx.tool_call_id,
                "result": "error",
                "error_type": type(error).__name__,
            },
        )

        return {
            "status": "error",
            "error": "Repeated requests could not be analyzed.",
        }