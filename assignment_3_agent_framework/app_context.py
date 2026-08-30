from dataclasses import dataclass


@dataclass
class AppContext:
    """Lokální kontext sdílený během jednoho běhu Agenta."""

    # Spojuje běh Agenta se všemi jeho auditními a nástrojovými událostmi.
    run_id: str

    # Identita je lokální aplikační údaj a neposílá se automaticky modelu.
    user_id: str = "local-user"